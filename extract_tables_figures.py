import sys
import json
import math
from dataclasses import dataclass
from pathlib import Path
from PIL import Image
import fitz


@dataclass
class TextBlock:
    x1: float
    y1: float
    x2: float
    y2: float
    text: str


# yolov8の結果（画像とlabels）から，図の領域を切り出してcaptionを探す
def main(path: str):
    path = Path(path)
    for name in ("tables", "figures"):
        out_path = path / name
        if not out_path.exists():
            out_path.mkdir()

    for text_file in (path / "labels").glob("*.txt"):
        print(text_file)
        image_file = path / f"images/{text_file.name[:-3]}png"
        image = Image.open(str(image_file))
        pdf_file = Path(path / text_file.name[:-8])
        page_index = int(text_file.name[-7:-4])
        pdf_doc = fitz.open(str(pdf_file))
        pdf_page = pdf_doc[page_index]
        text_blocks = pdf_page.get_text('blocks')  # text_block: tuple of (x1, y1, x2, y2, text, _, _)
        fig_blocks = [TextBlock(b[0], b[1], b[2], b[3], b[4]) for b in text_blocks if b[4].startswith("Figure")]
        tab_blocks = [TextBlock(b[0], b[1], b[2], b[3], b[4]) for b in text_blocks if b[4].startswith("Table")]

        with open(str(text_file), encoding="utf-8") as f:
            lines = f.readlines()

        tab_count = 0
        fig_count = 0
        for line in lines:
            items = line.strip().split(" ")
            x, y, w, h = float(items[1]), float(items[2]), float(items[3]), float(items[4])
            x1, x2 = x - w / 2, x + w / 2
            y1, y2 = y - h / 2, y + h / 2

            label = items[0]
            assert label == "0" or label == "1"  # "0": table, "1": figure
            w, h = image.width, image.height
            image_bbox = math.floor(x1 * w), math.floor(y1 * h), math.ceil(x2 * w), math.ceil(y2 * h)
            w, h = pdf_page.rect.width, pdf_page.rect.height
            pdf_bbox = x1 * w, y1 * h, x2 * w, y2 * h

            if label == "0":
                out_image_file = path / f"tables/{image_file.name[:-4]}_{tab_count:02}.png"
                block = find_caption(tab_blocks, pdf_bbox, "t")
            elif label == "1":
                out_image_file = path / f"figures/{image_file.name[:-4]}_{fig_count:02}.png"
                block = find_caption(fig_blocks, pdf_bbox, "b")
            else:
                raise Exception("not table nor figure")
            if block is None:
                caption = ""
            else:
                caption = block.text.replace("\n", "")

            image.crop(image_bbox).save(out_image_file)
            with open(str(out_image_file)[:-3] + "txt", "w", encoding="utf-8") as f:
                f.write(caption)
            if label == "0":
                tab_count += 1
            elif label == "1":
                fig_count += 1


def find_caption(blocks: list[TextBlock], bbox: tuple, direction: str):
    # direction: "t": top, "b": bottom
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    nearest_block = None
    min_gap = 50  # 50 の閾値は適宜調整する
    for b in blocks:
        if direction == "t":
            gap = y1 - b.y2
        elif direction == "b":
            gap = b.y1 - y2  # text blockとbboxがどのくらい離れているか？
        else:
            raise Exception("invalid direction")
        if b.x1 <= cx <= b.x2 and 0 < gap < min_gap:
            # if nearest_block is None or nearest_block.y1 > b.y1:
            nearest_block = b
            min_gap = gap
    return nearest_block


if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
