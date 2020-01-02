
import hashlib
import re
import sys
from PyQt5 import  QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import copy
import numpy as np


from PIL import Image   


def sliding_window(image, stepSize, windowSize):#参数1：要检查的对象 参数2：每次跳过多少像素，参数3：每次窗口要检查的大小
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])