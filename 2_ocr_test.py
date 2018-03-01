# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image


im = Image.open('1.png')
data = pytesseract.image_to_string(im)
print(data)
