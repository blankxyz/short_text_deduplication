#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2019-07-30
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
"""

import json
import codecs
import numpy as np

basic_dir = r'E:\workspace_python\jupyter_workspace\diary for eseence securities\文本去重'

# 读入源文件
file_segment_a = basic_dir+'/data/segment_answer_unique_20190719.json'
file_segment_q = basic_dir+'/data/segment_question_unique_20190719.json'
file_stop_words = basic_dir+'/data/stop_words.txt'
file_map_qa = basic_dir+'/data/unique_map_qa.txt'

# 问题
with codecs.open(file_segment_q, 'r', 'utf-8') as f:
    q_unique = json.load(f)

# 回答
with codecs.open(file_segment_a, 'r', 'utf-8') as f:
    a_unique = json.load(f)

# 问答映射
with codecs.open(file_map_qa, 'r', 'utf-8') as f:
    map_qa = json.load(f)

# 停用词
with codecs.open(file_stop_words, 'r', 'utf-8') as f:
    stop_words = f.read()
    stop_words = stop_words.splitlines()

import gensim
#载入词向量
file_word2vec = basic_dir+'/data/word_set_embedding_gensim.txt'
model = gensim.models.KeyedVectors.load_word2vec_format(file_word2vec, binary=False)



# 计算
# 句向量计算函数
#==============词向量求平均===================
def sentenceByWordVectAvg(sentence,model,embeddingSize):
    # 将所有词向量的woed2vec向量相加到句向量
    sentenceVector = np.zeros(embeddingSize)
    # 计算每个词向量的权重，并将词向量加到句向量
    for word in sentence:
        if word not in model.vocab:
            continue
        sentenceVector = np.add(sentenceVector, model[word])
    if len(sentence)>0:
        sentenceVector = np.divide(sentenceVector,len(sentence))
    return sentenceVector



# 过程性函数
def cal_sentence2vec(sentences, model, embedding_size, method="average"):
    result = {}
    if method == "average":
        for sentence in sentences:
            index = sentence[0]
            s2v = sentenceByWordVectAvg(sentence=sentence[1], model=model, embeddingSize=embedding_size)
            result[index] = s2v
    return result

# 平均词向量
q_average_s2v = cal_sentence2vec(q_unique['data'], model, 200, method="average")
a_average_s2v = cal_sentence2vec(a_unique['data'], model, 200, method="average")

# 使用pandas计算相关系数矩阵
import time
import pandas as pd
t1 = time.time()
df_a = pd.DataFrame(a_average_s2v)
t2 = time.time()
print(u'生成df 耗时 {0} secs'.format(t2-t1))
coef = df_a.corr()
t3 = time.time()
print(u'相关系数计算 耗时 {0} secs'.format(t3-t2))
coef_single = df_a.corrwith(df_a.iloc[:, 0])
t4 = time.time()
print(u'单个输入相关系数矩阵计算 耗时 {0} secs'.format(t4-t3))

# 基于numpy的计算
# 使用numpy计算相关系数
t5 = time.time()
# 获取index map
a_keys = a_average_s2v.keys()
map_a_to_index = {}
map_index_to_a = {}
array_a = []
for index, k in enumerate(a_keys):
    map_index_to_a[index] = k
    map_a_to_index[k] = index
    array_a.append(a_average_s2v[k])
array_a = np.asarray(array_a)
t6 = time.time()
print(u'生成 np.array 耗时 {0} secs'.format(t6-t5))
coef_np = np.corrcoef(array_a)
t7 = time.time()
print(u'相关系数计算 耗时 {0} secs'.format(t7-t6))

def corr2_coeff(A,B):
    """
        两个矩阵的的相关系数矩阵
    :param A: 新矩阵
    :param B: 已有矩阵
    :return: 相关系数矩阵
    """
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:,None]
    B_mB = B - B.mean(1)[:,None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1);
    ssB = (B_mB**2).sum(1);

    # Finally get corr coeff
    return np.dot(A_mA,B_mB.T)/np.sqrt(np.dot(ssA[:,None],ssB[None]))


# 载入数据
dataset = {}
index = 0
for k, v in q_unique_dict.items():
    q_id = k
    q = ''.join(v)
    q_seg = v

    qa = map_qa['q_{}'.format(q_id)]

    classify = qa['classify']
    a_id = qa['a_id']
    a_seg = a_unique_dict[a_id]
    a = ''.join(a_seg)
    text = {'classify': classify,
            'q_id': q_id,
            'q_seg': q_seg,
            'q': q,
            'a_id': a_id,
            'a_seg': a_seg,
            'a': a}
    dataset[index] = text
    index += 1


import pandas as pd
df = pd.read_excel()

if __name__ == '__main__':
    """
        涉及变量
         q_unique_dict
         a_unique_dict
         map_qa: qa映射
         stop_words
         
         q_average_s2v dict
         a_average_s2v 
       
         map_data_to_index
         map_index_to_data
         coef_np  
    """
    pass
    pd.DataFrame()
