from pathlib import Path

from ultralytics import YOLO
from PIL import Image


def run():
    model = YOLO("yolov8x.pt")
    model.train(data="publaynet-figure.yaml", epochs=100, batch=224, device=[0, 1, 2, 3])  # imgsz=800
    # model = YOLO("/home/shindo/Documents/GitHub/hshindo/docparse/runs/detect/train16/weights/last.pt")
    # model.train(resume=True)


def predict():
    model = YOLO("best.pt")
    # model.export(format="onnx", imgsz=800)

    for file in Path("../.data/bert-png").glob("*.png"):
        image = Image.open(str(file))
        results = model.predict(source=image, save=True, save_txt=True, device="cpu")  # imgsz=800


if __name__ == "__main__":
    run()
    # predict()
