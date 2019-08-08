#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 生成分好词的待去重文本 segment_xxx_unique.json 及
           对应的总词表大小文件
Created on 201
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
"""
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import codecs
import json
import collections
import time

from settings import *
from utils import nlp_utils


# 获取待计算文本
def _read_data(filepath=None):
    # 读文件
    if not filepath:
        raise BaseException(r'缺少文件路径和文件名')
    with codecs.open(filepath, 'r', conf.data_encoding) as f:
        data = json.load(f)
    data = data['data']
    # 分词及统计词频
    data_segment = []
    data_count = collections.Counter()
    for d in data:
        _segment = nlp_utils.segment(d[1])
        data_segment.append([d[0], _segment])
        for w in _segment:
            data_count[w] += 1
    return data_segment, data_count

# 1.获取数据
def get_data(method='question'):
    t1 = time.time()
    print(r'= {0}'.format(method))
    if method not in ['question', 'answer']:
        raise BaseException(r'方法参数错误 只能在 question和answer中')
    # 1.获取待计算文本及分词获取所需词表
    if method == 'question':
        file_input = conf.file_question_unique
    if method == 'answer':
        file_input = conf.file_answer_unique
    data_segment, data_count = _read_data(filepath=os.path.join(conf.basic_path, file_input))
    j1 = {'data':data_segment} # 分好词的文件
    print(u'总共需要的单词数 {0}'.format(len(data_count.keys())))
    with codecs.open(os.path.join(conf.basic_path, 'segment_'+file_input), 'w', 'utf-8') as f:
        json.dump(j1, f)
    t2 = time.time()
    print(u'{0} 分词数据文件=生成 耗时 {1} mins'.format(method, (t2-t1)/60))
    return data_segment, list(data_count.keys())

# 2.

# 主程序
def main():
    method = ['answer', 'question']
    words = []
    for m in method:
        _, _words = get_data(method=m)
        words += _words
    words = list(set(words))

    with codecs.open(os.path.join(conf.basic_path, conf.file_path_words_set), 'w', 'utf-8') as f:
        f.write('\n'.join(words))

if __name__ == '__main__':
    main()