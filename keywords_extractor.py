import os
from class_info import Class_info
from load_data import load_data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np


class Keywords_File:
    filename = ""
    keywords = []
    tfidf =[]

    def __init__(self, filename, keywords=[], tfidf=[]):
        self.filename = filename
        self.keywords = keywords
        self.tfidf = tfidf
'''
corpus = []

folder = "pre_swift"  # 文件夹目录
filenames = os.listdir(folder)  # 得到文件夹下的所有文件名称
for filename in filenames:  # 遍历文件夹
    if not os.path.isdir(filename):  # 判断是否是文件夹，不是文件夹才打开
        obj = load_data(folder + "/" + filename)
        result = ' '.join(obj.class_description+obj.class_name)
        corpus.append(result)

vectorizer = CountVectorizer()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

word = vectorizer.get_feature_names()  # 所有文本的词
weight = tfidf.toarray()  # 对应的tfidf矩阵

n = 10
f = open('tfidf_swift.txt', 'w+')
keywords_filelist = []
for (filename, w) in zip(filenames, weight):
    print(filename)
    kw = Keywords_File(filename)
    wordslist = []
    tfidf_list = []
    f.write(filename+"\n")
    loc = np.argsort(-w)
    for i in range(n):
        print(u'-{}: {} {}'.format(str(i+1), word[loc[i]], w[loc[i]]))
        f.write(u'-{}: {} {}'.format(str(i+1), word[loc[i]], w[loc[i]])+"\n")
        wordslist.append(word[loc[i]])
        tfidf_list.append(w[loc[i]])
    f.write("\n")
    kw.keywords = wordslist
    kw.tfidf = tfidf_list
    keywords_filelist.append(kw)
f.close()
np.save("keywords_swift.npy", keywords_filelist)
'''


n = 10   # 提取的关键词数量
def extract_keywords(filename, index, corpus):
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()  # 所有文本的词
    weight = tfidf.toarray()  # 对应的tfidf矩阵

    w = weight[index]
    kw = Keywords_File(filename)
    wordslist = []
    tfidf_list = []
    loc = np.argsort(-w)
    for i in range(n):
        wordslist.append(word[loc[i]])
        tfidf_list.append(w[loc[i]])
    kw.keywords = wordslist
    kw.tfidf = tfidf_list
    return kw
