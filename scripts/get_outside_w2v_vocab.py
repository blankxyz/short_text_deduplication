#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 获取外部词向量词表
Created on 2019-07-17
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
"""
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import codecs
from tqdm import tqdm

from settings import *


def main(filepath=None, start_step=0):
    if not filepath:
        filepath = conf.file_path_word2vec
    with codecs.open(filepath, 'r', conf.data_encoding) as f:
        # 总词表大小和维数
        num_vocab, dim = f.readline().split(' ')
        # print('单词数 {0}  词向量size {1}'.format(num_vocab, dim))
        vocab = []
        for index in tqdm(range(int(num_vocab))):
            data = f.readline()
            if index < start_step:
                continue
            data = data.split(' ')[0]
            if data == '\n':
                data=r'\\n'
                print(r'\n 存在 '+ str(index))
            vocab.append(data)
            if (index+1) % 2000 == 0 and vocab:
                with codecs.open(os.path.join(conf.basic_path, conf.file_path_word2vec_vocab), 'a', conf.data_encoding) as m:
                    m.write('\n'.join(vocab))
                    m.write('\n')
                vocab = []
        if vocab:
            with codecs.open(os.path.join(conf.basic_path, conf.file_path_word2vec_vocab), 'a',
                             conf.data_encoding) as m:
                m.write('\n'.join(vocab))
    pass

if __name__ == '__main__':
    main(start_step=0)
    pass