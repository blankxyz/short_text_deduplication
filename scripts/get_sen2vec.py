#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2019-07-17
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
    计算文本集中的每个短文本的句向量
"""
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import codecs
import jieba

from settings import *


# 1.获取待计算文本
def get_data(filepath=None):
    if not filepath:
        filepath = os.path.join(conf.basic_path, conf.file_question_unique)
    with codecs.open(filepath, 'r', conf.data_encoding) as f:
        data = f.readlines()
    data = data.splitlines()
    data = [d.split(conf.data_sep) for d in data]

    return data

# 2.分词获取所需词表


# 主程序
def main():
    # 1.获取待计算文本
    data = get_data()
    # 2.分词获取所需词表
    pass

if __name__ == '__main__':
    # main()
    read_data()
    pass
