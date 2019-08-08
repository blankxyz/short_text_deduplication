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
import time
from tqdm import tqdm
import json
import re

from settings import *
import src.calculate as cal


# 1.加载词向量文件
def load_word2vec():
    embedding_index = {}
    _file_dir = conf.file_path_word2vec
    with codecs.open(_file_dir, 'r', conf.data_encoding) as f:
        # 总词表大小和维数
        num_vocab, dim = f.readline().split(' ')
        # for index in tqdm(range(int(500))):
        for index in tqdm(range(int(num_vocab))):
            line = f.readline()
            values = line.split(' ')
            if index % 2000 == 0:
                print('{0} {1}'.format(index, values[0]))
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = coefs
    return embedding_index, int(dim)

# 2.批量生成待计算的句向量
def _get_word_embedding(w, embedding_index, embedding_size):
    _w = [w, w.lower(), w.upper()]
    for i in _w:
        res = embedding_index.get(i, None)
        if type(res) == np.ndarray:
            res = res.tolist()
            return res
    res = [0.0]*embedding_size
    return res


def produce_batch_word_set_embedding(embedding_index, embedding_size, batch_size=500):
    # 待查询的词表地址 words_set
    _file_dir = os.path.join(conf.basic_path, conf.file_path_words_set)
    # 查询后词表及词向量输出地址
    _file_out_dir = os.path.join(conf.basic_path, 'word_set_embedding.txt')
    # 未知词表地址
    _file_out_noembedding_dir = os.path.join(conf.basic_path, 'word_set_no_embedding.txt')
    # 后两者文件如果存在则删除
    for _file_path in [_file_out_dir, _file_out_noembedding_dir]:
        if os.path.exists(_file_path):
            os.remove(_file_path)

    with codecs.open(_file_dir, 'r', conf.data_encoding) as f:
        data = []
        t1 = time.time()
        batch_index = 0
        for index, line in enumerate(f):
            # if index >1200:
            #     return
            # 没 batch_size 个数据写入文件一次
            if (index+1) % batch_size == 0:
                batch_index += 1
                with codecs.open(_file_out_dir, 'a', conf.data_encoding) as f2:
                    f2.write('\n'.join(data)+'\n')
                data = []
                t2 = time.time()
                print(u'生成待定embedding词表====>batch {0} 耗时 {1} mins'.format(batch_index, (t2-t1)/60.0))
                t1 = t2
            line = re.sub('\n+$', '', line)
            w2v = _get_word_embedding(w=line, embedding_index=embedding_index, embedding_size=embedding_size)
            line_data = {line: w2v}
            data.append(json.dumps(line_data))
        if data != []:
            with codecs.open(_file_out_dir, 'a', conf.data_encoding) as f2:
                f2.write('\n'.join(data)+'\n')
    return


# 主函数
def main():
    # 1. 加载外部词向量
    t1 = time.time()
    embedding_index, embedding_size = load_word2vec()
    t2 = time.time()
    print(u'加载词向量 耗时 {0} mins'.format((t2 - t1) / 60))

    # 2. 批量生成生成待定词向量
    produce_batch_word_set_embedding(embedding_index=embedding_index,
                                     embedding_size=embedding_size,
                                     batch_size=500)
    t3 = time.time()
    print(u'生成待定embedding词表总耗时 {0} mins'.format((t3 - t2) / 60.0))
    return

if __name__ == '__main__':
    main()

