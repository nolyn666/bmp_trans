import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data
import random
from aesfunc import PrpCrypt
import binascii

img = cv2.imread("123.bmp")
# img = cv2.resize(img, (448, 448))
# 将多通道图像变为单通道图像
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)

# Wavelet transform of image, and plot approximation and details
titles = ['Approximation', ' Horizontal detail',
          'Vertical detail', 'Diagonal detail']
coeffs2 = pywt.dwt2(img, 'bior1.3')
LL, (LH, HL, HH) = coeffs2

fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()
# 32位密钥
pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥
dict = {'1': '4', '2': '9', '3': '5', '4': '1',
        '5': '7', '6': '8', '7': '2', '8': '3', '9': '6', '0': '0', '-': '-'}


def encryptll(dict, l_item):
    l_str = str(l_item)
    ll_str = ''
    for i in l_str:
        if i != '.':
            ll_str += dict[i]
        else:
            ll_str += '.'
    return float(ll_str)

# e_hex = binascii.hexlify(e) # 转
    e_str = e.decode()  # 十六进制字节流转字符串
    return sum([ord(a) for a in e_str])  # 字符串asiic码求和


def decryptll(dict, l_item):

    d = pc.decrypt(e)  # 解密a

cou=len(LL)*len(LL[0])
trans_list = [i for i in range(cou//2,cou)]
random.shuffle(trans_list)

# 加密
plt.figure('二维小波一级变换')
for i in range(len(LL)//2):
    for j in range(len(LL[0])):
        pos=i*len(LL[0])+j # 像素点的位置
        row =trans_list[pos]//len(LL[0]) # 与当前像素对换的像素行号
        column =trans_list[pos]%len(LL[0]) # 与当前像素对换的像素列号
        temp=LL[i][j]
        LL[i][j]=LL[row][column]
        LL[row][column]=temp
    # print('\n')
    # print(len(LL[i]))
#     for j in range(len(LL[i])):
plt.subplot(221), plt.imshow(LL, 'gray'), plt.title("A")
plt.show()

# 解密
plt.figure('二维小波一级变换')
for i in range(len(LL)//2):
    for j in range(len(LL[0])):
        pos=i*len(LL[0])+j # 像素点的位置
        row =trans_list[pos]//len(LL[0]) # 与当前像素对换的像素行号
        column =trans_list[pos]%len(LL[0]) # 与当前像素对换的像素列号
        temp=LL[i][j]
        LL[i][j]=LL[row][column]
        LL[row][column]=temp
    # print('\n')
    # print(len(LL[i]))
#     for j in range(len(LL[i])):
plt.subplot(221), plt.imshow(LL, 'gray'), plt.title("A")
plt.show()

# plt.figure('二维小波一级变换解密')
# for i in range(len(LL)):
#     for j in range(len(LL[i])):
#         LL[i][j] = decryptll(pc, LL[i][j])

# plt.subplot(221), plt.imshow(LL, 'gray'), plt.title("A")
# plt.show()
# d = pc.decrypt(e)  # 解密
# print("加密:", e)
# print("解密:", d)