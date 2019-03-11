# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:25:17 2019

@author: ztw
"""

from preprocessor import preprocess
import os
from load_data import load_data
from load_data import get_corpus
from keywords_extractor import extract_keywords
import numpy as np

language = "swift"   # 文件夹目录
filenames = os.listdir(language)   # 得到文件夹下的所有文件名称
'''
for filename in filenames:   # 遍历文件夹
    if not os.path.isdir(filename):   # 判断是否是文件夹，不是文件夹才打开
        preprocess(load_data(language+"/"+filename), filename, language)
'''

corpus = get_corpus(language)
index = 0
keywords_filelist = []
pre_filenames = os.listdir("pre_swift")
for filename in pre_filenames:
    if not os.path.isdir(filename):
        kw = extract_keywords(filename, index, corpus)
        keywords_filelist.append(kw)
        index += 1
        # print(filename)
np.save("keywords_swift.npy", keywords_filelist)
