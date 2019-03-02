# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:25:17 2019

@author: ztw
"""

from preprocessor import preprocess
import os
from load_data import load_data

language = "swift"   # 文件夹目录
filenames = os.listdir(language)   # 得到文件夹下的所有文件名称
for filename in filenames:   # 遍历文件夹
    if not os.path.isdir(filename):   # 判断是否是文件夹，不是文件夹才打开
        print(filename)
        preprocess(load_data(language+"/"+filename), filename, language)

# preprocess(load_data("Dictionary.json"), "Dictionary.json")
