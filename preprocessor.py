# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:29:28 2019

@author: ztw
"""
import re
import json
import class_info
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import nltk.data


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
other_re = re.compile('[^a-zA-Z0-9_ ]')
stop_words = set(stopwords.words('english'))
porter_stemmer = PorterStemmer()


# 处理包名
def process_package(string):
    string = string.replace('.', ' ')
    word_tokens = word_tokenize(string)  # 分词
    for i in range(len(word_tokens)):
        word_tokens[i] = porter_stemmer.stem(word_tokens[i])  # 基于Porter词干提取算法
    return word_tokens


def split_camelcase_notation(string):
    #print(type(string))
    string = other_re.sub('', string)   # 先去除额外的字符
    s1 = first_cap_re.sub(r'\1 \2', string)
    return all_cap_re.sub(r'\1 \2', s1).lower()


# 处理名字和类型
def process_name_and_type(string):
    string = split_camelcase_notation(string)
    string = other_re.sub('', string).lower()  # 先去除额外的字符并转小写
    word_tokens = word_tokenize(string)  # 分词
    for i in range(len(word_tokens)):
        word_tokens[i] = porter_stemmer.stem(word_tokens[i])  # 基于Porter词干提取算法
    return word_tokens


# 分句
def splitSentence(paragraph, num):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    count = min(num, len(sentences))
    return_string = ""
    for index in range(count):
        return_string += sentences[index]
    return return_string


# 处理描述性文字（按需取段落的前几句）
def process_description(string, language, num=-1):
    if language == "java":
        string = splitSentence(string, num)  # 取段落的前2句或前5句
    string = other_re.sub('', string).lower()  # 先去除额外的字符并转小写
    word_tokens = word_tokenize(string)  # 分词
    str_array = [w for w in word_tokens if w not in stop_words]  # 除去停止词
    for i in range(len(str_array)):
        str_array[i] = porter_stemmer.stem(str_array[i])   # 基于Porter词干提取算法
    return str_array


def preprocess(obj, filename, language):
    obj.package_name = process_package(obj.package_name)
    obj.class_name = process_name_and_type(obj.class_name)
    obj.class_description = process_description(obj.class_description, 5)
    # print(obj.class_description)

    for i in range(len(obj.class_inherit_list)):
        obj.class_inherit_list[i] = process_name_and_type(obj.class_inherit_list[i])
    for i in range(len(obj.interface_list)):
        obj.interface_list[i] = process_name_and_type(obj.interface_list[i])
    for i in range(len(obj.subclass_list)):
        obj.subclass_list[i] = process_name_and_type(obj.subclass_list[i])

    for i in range(len(obj.Methods)):
        method = obj.Methods[i]
        # print(i)

        obj.Methods[i].class_name = process_name_and_type(method.class_name)
        obj.Methods[i].method_name = process_name_and_type(method.method_name)
        obj.Methods[i].method_description = process_description(obj.Methods[i].method_description, language, 2)

        for j in range(len(method.params)):
            obj.Methods[i].params[j].param_type = process_name_and_type(method.params[j].param_type)
            for z in range(len(method.params[j].param_name)):
                obj.Methods[i].params[j].param_name[z] = process_name_and_type(method.params[j].param_name[z])
            obj.Methods[i].params[j].param_description = process_description(obj.Methods[i].params[j].param_description, language, 2)
        obj.Methods[i].params = class_info.convert_to_dicts(obj.Methods[i].params)
        
        # print(len(method.return_value.return_type))
        for j in range(len(method.return_value.return_type)):
            obj.Methods[i].return_value.return_type[j] = process_name_and_type(method.return_value.return_type[j])
        for j in range(len(method.return_value.return_name)):
            if isinstance(obj.Methods[i].return_value.return_name[j],str):
                obj.Methods[i].return_value.return_name[j] = process_name_and_type(method.return_value.return_name[j])
            if isinstance(obj.Methods[i].return_value.return_name[j], list):
                for z in range(len(obj.Methods[i].return_value.return_name[j])):
                    obj.Methods[i].return_value.return_name[j][z] = process_name_and_type(method.return_value.return_name[j][z])
        for j in range(len(method.return_value.return_description)):
            obj.Methods[i].return_value.return_description[j] = process_description(obj.Methods[i].return_value.return_description[j], language, 2)
        return_value_dict = {}
        return_value_dict.update(obj.Methods[i].return_value.__dict__)
        obj.Methods[i].return_value = return_value_dict

    for i in range(len(obj.Vars)):
        obj.Vars[i].var_name = process_name_and_type(obj.Vars[i].var_name)
        obj.Vars[i].var_type = process_name_and_type(obj.Vars[i].var_type)
        obj.Vars[i].var_description = process_description(obj.Vars[i].var_description, language, 2)

    obj.Methods = class_info.convert_to_dicts(obj.Methods)
    obj.Vars = class_info.convert_to_dicts(obj.Vars)

    obj_dict = {}
    obj_dict.update(obj.__dict__)
    json_str = json.dumps(obj_dict)
    fh = open("pre_"+language+"/"+filename, 'w')
    fh.write(json_str)
    fh.close()
