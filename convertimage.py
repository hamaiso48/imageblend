import os
from pathlib import Path
from pdf2image import convert_from_path

class convertImage:
    def __init__(self, pdf_Path):
        self.pdf_Path = pdf_Path
        # self.output_image = output_File

    def convert(self):
        # poppler/binを環境変数PATHに追加する
        poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
        os.environ["PATH"] += os.pathsep + str(poppler_dir)

        # PDF -> Image に変換（150dpi）
        pages = convert_from_path(str(self.pdf_Path), 150)

        # 画像ファイルを１ページずつ保存
        image_dir = Path("./images")
        for i, page in enumerate(pages):
            file_name = Path(self.pdf_Path).stem + "_{:02d}".format(i + 1) + ".jpeg"
            image_path = image_dir / file_name
            # JPEGで保存
            page.save(str(image_path), "JPEG")
            # 1ページ目だけで止める
            if(i==0):
                break
        
        return image_path
    
def main(pdf_path):
    convert = convertImage(pdf_path)
    return convert.convert()

if __name__ == "__main__":
    main()
