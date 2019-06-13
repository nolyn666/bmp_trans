# BMP图像加解密与小波变换

## 依赖

名称|版本
-|-
numpy|latest
opencv|latest
pywavelet|latest


## 功能

* 对给定路径下的所有BMP图像(遍历子目录)进行迭代
* 对图像进行小波变换,并加密其低频系数
* 加解密图像


## 参数

名称|类型|含义
-|-|-
pathname|string|需要加密的文件夹路径
mode|string|e:加密 d:解密
key|string|密钥


## 运行

`python3 wavelet.py`