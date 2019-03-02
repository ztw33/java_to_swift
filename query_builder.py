# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 20:58:13 2019

@author: ztw
"""
from load_data import load_data
from preprocessor import preprocess

language = "java"
filename = "String.json"
preprocess(load_data(language+"/"+filename), filename, language)
