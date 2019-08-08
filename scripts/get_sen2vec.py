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
import numpy as np
import json
import pickle
import pandas as pd

from settings import *

# 1.加载词向量文件 -- word_set_embedding.txt
def load_words_set_embedding():
    embedding_index = {}
    _file_dir = os.path.join(conf.basic_path, 'word_set_embedding.txt')
    with codecs.open(_file_dir, 'r', conf.data_encoding) as f:
        data = f.read()
    for d in data.splitlines():
        _d = json.loads(d)
        embedding_index.update(_d)
    return embedding_index

# 2.加载待计算文件
def get_file_segment(method='question'):
    res = {}
    _file_dir = ''
    if method == 'question':
        _file_dir = os.path.join(conf.basic_path, conf.file_segment_question_unique)
    if method == 'answer':
        _file_dir = os.path.join(conf.basic_path, conf.file_segment_answer_unique)
    if _file_dir == '':
        return res
    with codecs.open(_file_dir, 'r', conf.data_encoding) as f:
        data = f.read()
    data = json.loads(data)
    return data['data']

# 3.计算句向量
def get_sentence2vector(s, embedding_index, embedding_size):
    num = embedding_size
    cum_vec = np.asarray([0]*num, dtype='float32')
    len_word = 0
    for w in s:
        sen2vec = _get_word_embedding(w=w, embedding_index=embedding_index, embedding_size=embedding_size)
        if np.linalg.norm(sen2vec) > 0:
            cum_vec += np.asarray(sen2vec)
            len_word += 1
    res = cum_vec/float(len_word)
    return res


def _get_word_embedding(w, embedding_index, embedding_size):
    _w = [w, w.lower(), w.upper()]
    for i in _w:
        res = embedding_index.get(i, None)
        if type(res) == list:
            return res
    res = [0.0]*embedding_size
    return res

def get_origin_data(method='question'):
    _file_dir = ''
    res = {}
    if method == 'question':
        _file_dir = os.path.join(conf.basic_path, conf.file_question_unique)
    if method == 'answer':
        _file_dir = os.path.join(conf.basic_path, conf.file_answer_unique)
    if _file_dir:
        with codecs.open(_file_dir, 'r', conf.data_encoding) as f:
            data = json.load(f)
        data = data['data']
        for d in data:
            res[d[0]] = d[1]
    return res

# 主函数
def main(schema=0.8):
    '''
    :param schema: 相关系数的阈值
    :return:
    '''
    # 1.获取词向量文件
    embedding_index = load_words_set_embedding()
    # 2.计算待计算文件句向量
    for m in ['question', 'answer']:
        print(u'计算 {0} 句向量'.format(m))
        data = get_file_segment(method=m)
        data_index_map = []
        data_s2v = []
        for d in data:
            index = d[0]
            s2v = get_sentence2vector(d[1], embedding_size=conf.embedding_size,
                                      embedding_index=embedding_index)
            data_index_map.append(index)
            data_s2v.append(s2v)
        print(u'保存 {0} 句向量文件 {0}_sentence2vector.json'.format(m))
        with codecs.open(os.path.join(conf.basic_path, '{0}_sentence2vector.dat'.format(m)), 'wb') as f:
            pickle.dump({'index': data_index_map, 'sentence2vector': data_s2v}, f)
            # try:
            #     json.dump({'index': data_index_map, 'sentence2vector': data_s2v}, f)
            # except:
            #     pass
        print(u'计算 {0} 句向量间的相关系数矩阵'.format(m))
        # 相关系数矩阵
        corrcoef = np.corrcoef(np.array(data_s2v))
        # 上三角
        U = np.triu(corrcoef, 1)
        cordient = np.where(U>schema)
        corcoef_list = U[U>schema]
        data_sentence_similary = []
        # 获取原始数据
        data_origin = get_origin_data(method=m)

        for n in range(corcoef_list.shape[1]):
            data_index_1 = data_index_map[cordient[0][n]]
            data_1 = data_origin[data_index_1]
            data_index_2 = data_index_map[cordient[1][n]]
            data_2 = data_origin[data_index_2]
            data_sentence_similary.append([data_index_map[cordient[0][n]],
                                           data_1,
                                           data_index_map[cordient[1][n]],
                                           data_2,
                                           corcoef_list[n]])

        pass
        # 保存词与index的映射表

    return


if __name__ == '__main__':
    main(schema=0.8)
