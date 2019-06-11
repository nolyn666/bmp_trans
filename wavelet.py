import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data
import random
import hashlib


class BmpBGR(object):

    def __init__(self, img_name):
        self.img_name = img_name
        self.B = None
        self.G = None
        self.R = None
        self.bgr_b = None
        self.bgr_g = None
        self.bgr_r = None
        self.load_img()
        self.trans_bgr()
        self.show_img()

    def load_img(self):
        """
        加载图片cv2
        :return: self.img
        """
        img = cv2.imread(self.img_name, 1)

        # 将多通道图像变为单通道图像
        (self.B, self.G, self.R) = cv2.split(img)
        self.B = self.B.astype(np.float32)
        self.G = self.G.astype(np.float32)
        self.R = self.R.astype(np.float32)

    def trans_bgr(self):
        bb = Bmpwave(self.B)
        self.bgr_b = bb.get_img()

        gg = Bmpwave(self.G)
        self.bgr_g = gg.get_img()

        rr = Bmpwave(self.R)
        self.bgr_r = rr.get_img()

    def show_img(self):
        img = cv2.merge([self.bgr_b, self.bgr_g, self.bgr_r])
        cv2.imwrite('111.bmp', img)
        # cv2.imwrite('222.bmp', img)


class Bmpwave(object):

    def __init__(self, img):
        self.trans_list = None
        self.img = img
        self.LL = None
        self.LH = None
        self.HL = None
        self.HH = None
        self.wavelet_trans()
        self.get_list()
        self.cryptobmp()
        self.wavelet_itrans()

    def get_list(self):
        try:
            f = open('./passwd.txt', 'r')
            self.trans_list = list(eval(f.read()))
        except:
            cou = len(self.LL) * len(self.LL[0])
            self.trans_list = [i for i in range(cou // 2, cou)]
            random.shuffle(self.trans_list)
            with open('./passwd.txt', 'w') as f:
                f.write(str(self.trans_list))
        finally:
            f.close()

    def wavelet_trans(self):
        """

        :return:
        """
        coeffs2 = pywt.dwt2(self.img, 'haar')
        self.LL, (self.LH, self.HL, self.HH) = coeffs2

    def wavelet_itrans(self):
        """

        :return:
        """
        coeffs2 = self.LL, (self.LH, self.HL, self.HH)
        self.img = pywt.idwt2(coeffs2, 'haar')

    def cryptobmp(self):
        for i in range(len(self.LL) // 2):
            for j in range(len(self.LL[0])):
                pos = i * len(self.LL[0]) + j  # 像素点的位置
                row = self.trans_list[pos] // len(self.LL[0])  # 与当前像素对换的像素行号
                column = self.trans_list[pos] % len(self.LL[0])  # 与当前像素对换的像素列号
                self.LL[i][j], self.LL[row][column] = self.LL[row][column], self.LL[i][j]

    def get_img(self):
        return self.img


if __name__ == '__main__':
    bmp = BmpBGR('123.bmp')
    # bmp = BmpBGR('111.bmp')
