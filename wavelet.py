import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data
import hashlib
from pathlib import Path


class Iter_bmps(object):

    def __init__(self, path_name, key, mode):
        """

        :param path_name: 文件夹路径
        :param key: 密钥
        :param mode: 模式:加密/解密
        """
        crypto_list = Cryptokey(key)
        self.crypto_list = crypto_list.get_crypto_list()  # 获取密钥序列
        self.path_name = path_name
        self.mode = mode
        self.iterallbmp()

    def iterallbmp(self):
        """
        遍历给定的目录,获取所有bmp格式图片的相对路径,并进行加密
        :return:
        """
        for item in Path(self.path_name).rglob('*.bmp'):
            BmpBGR(str(item), self.crypto_list, self.mode)


class BmpBGR(object):

    def __init__(self, img_name, crypto_list, mode):
        """

        :param img_name:图片名称
        :param crypto_list: 加密列表
        :param mode: 模式:加密/解密
        """
        self.mode = mode
        self.img_name = img_name
        self.crypto_list = crypto_list
        self.B = None
        self.G = None
        self.R = None
        self.bgr_b = None
        self.bgr_g = None
        self.bgr_r = None
        self.load_img()
        self.trans_bgr()
        self.save_img()

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
        bb = Bmpwave(self.img_name, self.B, self.crypto_list, self.mode)
        self.bgr_b = bb.get_img()

        gg = Bmpwave(self.img_name, self.G, self.crypto_list, self.mode)
        self.bgr_g = gg.get_img()

        rr = Bmpwave(self.img_name, self.R, self.crypto_list, self.mode)
        self.bgr_r = rr.get_img()

    def save_img(self):
        """
        合并图片的三个通道,存储图片
        :return:
        """

        img = cv2.merge([self.bgr_b, self.bgr_g, self.bgr_r])
        cv2.imwrite(self.img_name, img)
        print(self.img_name + "  Done")


class Bmpwave(object):

    def __init__(self, img_name, img, crypto_list, mode):
        self.img_name = img_name
        self.mode = mode
        self.trans_list = None
        self.img = img
        self.crypto_list = crypto_list
        self.LL = None
        self.LH = None
        self.HL = None
        self.HH = None
        self.trans_bmp()

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
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                salt = (self.crypto_list[i % 64] * self.crypto_list[j % 64]) % 256
                self.img[i][j] = (self.img[i][j] + salt) % 256

    def decryptobmp(self):
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                salt = (self.crypto_list[i % 64] * self.crypto_list[j % 64]) % 256
                self.img[i][j] = (self.img[i][j] - salt) % 256

    def get_img(self):
        """
        获取img
        :return: 图像对象
        """
        return self.img


class Cryptokey(object):

    def __init__(self, key):
        self.key = key
        self.crypto_list = None
        self.sha256fun()

    def sha256fun(self):
        m2 = hashlib.sha256()
        m2.update(self.key.encode('utf-8'))
        self.crypto_list = [int(ord(x)) for x in m2.hexdigest()]

    def get_crypto_list(self):
        return self.crypto_list


if __name__ == '__main__':
    key = input("please input your key:")
    mode = input("input 'e' to encrypto or 'd' to decrypto, others for exit:")
    path = input("input the path that you want to crypto:")
    bmps = Iter_bmps(path, key, mode)
