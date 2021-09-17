from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

class imageBlend:
    def __init__(self, red_FilePath, blue_FilePath, output_File, preview_umu):
        self.red_dir = red_FilePath
        self.blue_dir = blue_FilePath
        self.output_image = output_File
        self.preview_umu = preview_umu

    def blendImage(self):
        src = Image.open(self.red_dir)
        mask = Image.open(self.blue_dir)

        # 配列化
        image_R = np.array(src)
        image_B = np.array(mask)

        # 輝度設定
        image_R[:, :, 0] = 255  # R -> 255
        image_B[:, :, 2] = 255  # B -> 255

        # 配列からImageオブジェクト
        image_R = Image.fromarray(image_R)
        image_B = Image.fromarray(image_B)

        self.resultImage = self.img_overray(image_R, image_B, 5)

    # 2つのイメージを重ね合わせ、一致する部分は黒くする。
    def img_overray(self, img1, img2, accuracy):
        img_merge = Image.blend(img1, img2, 0.5)

        dat_img_merge = np.array(img_merge)

        width, height = img_merge.size

        # 保存用イメージの配列作成
        saveimg = np.zeros((height, width, 3), np.uint8)

        # 重なる画素部はグレースケールをセットする
        for x in range(height):
            for y in range(width):
                r = dat_img_merge[x,y,0]
                g = dat_img_merge[x,y,1]
                b = dat_img_merge[x,y,2]

                if(r > b-accuracy and r < b+accuracy):
                    saveimg[x,y] = [b,b,b]
                else:
                    saveimg[x,y] = [r,g,b]

        return saveimg

    def show(self):

        # ファイル出力用にImage変換
        file_resultImage = Image.fromarray(self.resultImage)

        if self.preview_umu == 0:
            # 表示
            plt.imshow(self.resultImage)
            plt.show()
        else:
            # ファイル出力
            file_resultImage.save(self.output_image)

def main(red, blue, output, preview_umu):
    imageblend = imageBlend(red, blue, output, preview_umu)
    imageblend.blendImage()
    imageblend.show()

if __name__ == "__main__":
    main()