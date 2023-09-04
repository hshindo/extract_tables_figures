# Extract tables, figures and captions from PDF
PDFから、図表とキャプションを抽出します。主に論文や特許のPDFを対象としています。

### Setup
* Python 3.9+
* `pip install Pillow pymupdf pdf2image ultralytics`


### PDFを画像に変換
* データを置くディレクトリを、例えば`/data/path` とする。この中にpdfファイルを全て置く。
* 以下を実行する。
```
python pdf_to_image.py /data/path 72
```
* `/data/path` 内の全てのpdfファイルを一括処理する。
* `72`は、出力画像のdpiを表す（デフォルトは`72`）。値を増やすと画像サイズが大きくなるが、この後の図表抽出まで行う場合は、デフォルトの72を推奨する。
画像ファイルは，`/data/path/images` に保存される．


### 図表の領域を抽出
* [yolov8x_publaynet_tables_figures.pt](https://drive.google.com/file/d/19bOSWGX7hRjbZtYfgo3En1TnBXv8GcEH/view?usp=sharing) をダウンロードして、本プログラムのルートディレクトリに置く。
* 以下を実行する。
```
yolo predict model=yolov8x_publaynet_tables_figures.pt source=/data/path/images save_txt save=False
```
* `save=False`を省略すると、抽出した領域を可視化した画像ファイルも出力される。
* 結果は、`runs/detect/predict` 以下に出力されているので、その中の`labels` を`/data/path/labels` へコピーする。


### 図表の切り出しとキャプションを出力
* 以下を実行する。
```
python extract_tables_figures.py /data/path
```
* 結果は、`/data/path/tables`, `/data/path/figures` にそれぞれ出力される。
