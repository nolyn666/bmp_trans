import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data
import random
import math
import hashlib


class BmpBGR(object):

    def __init__(self, img_name, key, mode):
        self.mode = mode
        self.img_name = img_name
        crypto_list = Cryptokey(key)
        self.mylist = crypto_list.get_mylist()  # 获取密钥序列
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
        分离图片的三个通道
        :return:
        """
        img = cv2.imread(self.img_name, 1)

        # 将多通道图像变为单通道图像
        (self.B, self.G, self.R) = cv2.split(img)
        self.B = self.B.astype(np.float32)
        self.G = self.G.astype(np.float32)
        self.R = self.R.astype(np.float32)

    def trans_bgr(self):
        """
        依次对图像的BGR三个通道进行小波变换,并进行低频系数加密/解密,然后小波逆变换
        返回加密/解密后的图像
        :return:
        """
        bb = Bmpwave(self.img_name, self.B, self.mylist, self.mode, 'B')
        self.bgr_b = bb.get_img()

        gg = Bmpwave(self.img_name, self.G, self.mylist, self.mode, 'G')
        self.bgr_g = gg.get_img()

        rr = Bmpwave(self.img_name, self.R, self.mylist, self.mode, 'R')
        self.bgr_r = rr.get_img()

    def show_img(self):
        """
        合并图片的三个通道,存储图片
        :return:
        """
        img = cv2.merge([self.bgr_b, self.bgr_g, self.bgr_r])
        if self.mode == 'e':
            save_name = 'en_' + self.img_name
        elif self.mode == 'd':
            save_name = 'de_' + self.img_name
        cv2.imwrite(save_name, img)


class Bmpwave(object):

    def __init__(self, img_name, img, mylist, mode, color):
        self.img_name = img_name
        self.mode = mode
        self.color = color
        self.trans_list = None
        self.img = img
        self.mylist = mylist
        self.LL = None
        self.LH = None
        self.HL = None
        self.HH = None
        # self.wavelet_trans()
        self.trans_bmp()
        # self.wavelet_itrans()

    def wavelet_trans(self):
        """
        对图像的某一通道进行haar小波变换
        :return:
        """
        self.LL, (self.LH, self.HL, self.HH) = pywt.dwt2(self.img, 'haar')

    def wavelet_itrans(self):
        """
        对图像的某一通道进行haar小波逆变换
        :return:
        """
        self.img = pywt.idwt2((self.LL, (self.LH, self.HL, self.HH)), 'haar')

    def trans_bmp(self):
        if self.mode == 'e':
            self.cryptobmp()
            self.wavelet_trans()

            self.wavelet_itrans()

        elif self.mode == 'd':
            self.decryptobmp()
            self.wavelet_trans()

            self.wavelet_itrans()
        else:
            exit(1)

    def cryptobmp(self):
        """
        按照给定的序列,对图片进行像素级加密
        :return:
        """
        # print(len(self.img))
        # print(self.img[0])
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                salt = (self.mylist[i % 64] * self.mylist[j % 64]) % 256
                self.img[i][j] = (self.img[i][j] + salt) % 256
                # self.LL[i][j] = self.LL[i][j] % 510

    def decryptobmp(self):
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                salt = (self.mylist[i % 64] * self.mylist[j % 64]) % 256
                self.img[i][j] = (self.img[i][j] - salt) % 256
                # self.LL[i][j] =self.LL[i][j]  % 510

    def get_img(self):
        """
        获取img
        :return: 图像对象
        """
        return self.img


class Cryptokey(object):

    def __init__(self, key):
        self.key = key
        self.mylist = None
        self.sha256fun()

    def sha256fun(self):
        m2 = hashlib.sha256()
        m2.update(self.key.encode('utf-8'))
        self.mylist = [int(ord(x)) for x in m2.hexdigest()]

    def get_mylist(self):
        return self.mylist


if __name__ == '__main__':
    key = input("please input your key:")
    mode = input("input 'e' to encrypto or 'd' to decrypto, others for exit:")
    bmp = BmpBGR('en_1.bmp', key, mode)
    # bmp = BmpBGR('2.bmp')
