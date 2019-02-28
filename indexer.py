# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:25:17 2019

@author: ztw
"""
import json
import class_info
import preprocessor
import os


def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
        package_name = data['package_name']
        class_name = data['class_name']
        class_description = data['class_description']

        class_inherit_list = []
        for element in data['class_inherit_list']:
            class_inherit_list.append(element)
        interface_list = []
        for element in data['interface_list']:
            interface_list.append(element)
        subclass_list = []
        for element in data['subclass_list']:
            subclass_list.append(element)

        Methods = []
        for method in data['Methods']:
            method_class = class_info.Method()
            method_class.class_name = method['class_name']
            method_class.method_name = method['method_name']
            method_class.method_description = method['method_description']
            param_list = []
            for param in method['params']:
                param_list.append(class_info.Param(param['param_type'], param['param_name'], param['param_description']))
            method_class.params = param_list
            return_value = class_info.Return_value()
            return_value.return_description = method['return_value']['return_description']
            return_value.return_type = method['return_value']['return_type']
            return_value.return_name = method['return_value']['return_name']
            method_class.return_value = return_value
            Methods.append(method_class)

        Vars = []
        if data['Vars'] is not None:
                for var in data['Vars']:
                    Vars.append(class_info.Var(var['var_name'], var['var_type'], var['var_description']))

        obj = class_info.Class_info(package_name, class_name, class_description, class_inherit_list, subclass_list, interface_list, Methods, Vars)
        return obj


path = "swift"   # 文件夹目录
filenames = os.listdir(path)   # 得到文件夹下的所有文件名称
for filename in filenames:   # 遍历文件夹
    if not os.path.isdir(filename):   # 判断是否是文件夹，不是文件夹才打开
        print(filename)
        preprocessor.preprocess(load_data(path+"/"+filename), filename)

# preprocessor.preprocess(load_data("Dictionary.json"), "Dictionary.json")
