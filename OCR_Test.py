import tesserocr
from PIL import Image
import numpy as np


image = Image.open('captcha2.png')
result = tesserocr.image_to_text(image)
print(result)

result = tesserocr.file_to_text('captcha2.png')
print(result)


#打印图片维度
print(np.array(image).shape)
print(image.mode)

#转成灰度图
#image = image.convert('L')
#image.show()打开图片

#图片二值化
#image = image.convert('1')
#image.show()

#转成灰度图，根据阈值删图片中的干扰点
image = Image.open('captcha2.png')
image = image.convert('L')
threshold=110
array=np.array(image)
array = np.where(array > threshold,255,0)
image = Image.fromarray(array.astype('uint8'))
image.show()
print(tesserocr.image_to_text(image))
