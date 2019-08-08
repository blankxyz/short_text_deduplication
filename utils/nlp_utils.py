#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: nlp相关工具
Created on 2019-07-19
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
"""
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import jieba
import codecs
import time

from settings import *

t1 = time.time()
# 1.分词类 =====================================
# 是否加载外部字典
if conf.load_outside_dict:
    jieba.load_userdict(conf.file_path_outside_dict)

# 是否使用停用词表
stop_words = []
if conf.mv_stop_words:
    with codecs.open(conf.file_path_stop_words, 'r', 'utf-8') as f:
        stop_words = f.read()
    stop_words = stop_words.splitlines()

t2 = time.time()
print(u'nlp模块导入耗时 {0} mins'.format((t2-t1)/60))

# 分词
def segment(s):
    if not s == s or not s:
        s = ''
    if isinstance(s, str):
        s = str(s)
    res = [d for d in jieba.cut(s) if d not in stop_words]
    return res



