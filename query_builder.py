# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 20:58:13 2019

@author: ztw
"""
from load_data import load_data
from preprocessor import preprocess
import os
from load_data import get_corpus
from keywords_extractor import extract_keywords
import numpy as np
import functools

language = "java"
filenames = os.listdir(language)   # 得到文件夹下的所有文件名称
'''
for filename in filenames:   # 遍历文件夹
    if not os.path.isdir(filename):   # 判断是否是文件夹，不是文件夹才打开
        print(filename)
        preprocess(load_data(language+"/"+filename), filename, language)
'''

keywords_swift = np.load('keywords_swift.npy')

class SameKeywords:
    filename = ""
    keywords_list = []
    num_of_same_kw = 0

    def __init__(self, filename, keywords_list):
        self.filename = filename
        self.keywords_list = keywords_list
        self.num_of_same_kw = len(keywords_list)


def cmp(x, y):
    if x.num_of_same_kw < y.num_of_same_kw:
        return -1
    elif x.num_of_same_kw == y.num_of_same_kw:
        return 0
    else:
        return 1


corpus = get_corpus(language)

index = 0
keywords_filelist = []
pre_filenames = os.listdir("pre_java")
for filename in pre_filenames:
    same_keywords_filelist = []
    if not os.path.isdir(filename):
        kw = extract_keywords(filename, index, corpus)
        keywords_filelist.append(kw)
        for target in keywords_swift:
            inter = [i for i in kw.keywords if i in target.keywords]
            if len(inter) > 0:
                same_keywords_filelist.append(SameKeywords(target.filename, inter))
        index += 1
    same_keywords_filelist.sort(key=functools.cmp_to_key(cmp), reverse=True)
    f = open('same_kw_java/'+os.path.splitext(filename)[0]+".txt", 'w+')
    for k in same_keywords_filelist:
        f.write(os.path.splitext(k.filename)[0]+": "+str(k.num_of_same_kw)+"\n"+"[")
        f.write(', '.join(k.keywords_list))
        f.write("]\n\n")

