#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 计算类
Created on 2019-07-17
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
    各种计算
"""
import numpy as np

def cal_sentence2vec(s, embedding):
    return

def cal_sentenceByWordVectAvg(sentence,model,embeddingSize):
    """
        平均词向量计算句向量
    :param sentence: 单句子（分好词）
    :param model: gensim对象或词向量字典
    :param embeddingSize: 词向量大小
    :return:
    """
    # 将所有词向量的woed2vec向量相加到句向量
    sentenceVector = np.zeros(embeddingSize)
    # 计算每个词向量的权重，并将词向量加到句向量
    for word in sentence:
        if word not in model.vocab:
            continue
        sentenceVector = np.add(sentenceVector, model[word])
    if len(sentence) > 0:
        sentenceVector = np.divide(sentenceVector,len(sentence))# 注意分子不能为零
    return sentenceVector

#

# 句向量相似度计算
def cal_sentence_similarity(s1, s2):
    similarity = np.dot(s1, s2)/(np.linalg.norm(s1)*np.linalg.norm(s2))
    return similarity

# 计算相关系数矩阵
def cal_corr2_coeff(A,B):
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

