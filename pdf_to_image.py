import sys
from pathlib import Path
import fitz
from pdf2image import convert_from_path, convert_from_bytes


def main(path: str, dpi: int):
    out_path = Path(path) / "images"
    if not out_path.exists():
        out_path.mkdir()

    for pdf_file in Path(path).glob("*.pdf"):
        print(pdf_file)
        # try:
        # images = convert_from_path(str(pdf_file), dpi=dpi)
        # except:
        #     continue
        # for i, image in enumerate(images):
        #     image.save(f"{out_path}/{pdf_file.name}_{i:03}.png")
        try:
            doc = fitz.open(str(pdf_file))
        except:
            continue
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            pix.save(f"{out_path}/{pdf_file.name}_{i:03}.png")


if __name__ == "__main__":
    path = sys.argv[1]
    dpi = 72
    if len(sys.argv) > 2:
        dpi = int(sys.argv[2])
    main(path, dpi)
