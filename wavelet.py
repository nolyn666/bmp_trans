import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data
import random


class Bmpwave(object):

    def __init__(self, img_name):
        self.trans_list = None
        self.img_name = img_name
        self.img = None
        self.LL = None
        self.LH = None
        self.HL = None
        self.HH = None
        self.load_img()


    def make_list(self):
        cou = len(self.LL) * len(self.LL[0])
        self.trans_list = [i for i in range(cou // 2, cou)]
        random.shuffle(self.trans_list)

    def load_img(self):
        """
        加载图片
        :return: self.img
        """
        self.img = cv2.imread(self.img_name)

        # 将多通道图像变为单通道图像
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY).astype(np.float32)

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

    def showbmp(self):
        plt.imshow(self.img, 'gray')
        plt.show()


if __name__ == '__main__':
    bmp=Bmpwave('123.bmp')

    bmp.wavelet_trans()
    bmp.make_list()
    bmp.cryptobmp()
    bmp.wavelet_itrans()
    bmp.showbmp()

    bmp.wavelet_trans()
    bmp.cryptobmp()
    bmp.wavelet_itrans()
    bmp.showbmp()
