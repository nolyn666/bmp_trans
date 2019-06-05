import numpy as np
import matplotlib.pyplot as plt
import cv2
import pywt
import pywt.data

img = cv2.imread("123.png")
# img = cv2.resize(img, (448, 448))
# 将多通道图像变为单通道图像
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)

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
print(LL)