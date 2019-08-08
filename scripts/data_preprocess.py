#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 201
@author: David Yisun
@group: data
@e-mail: david_yisun@163.com
@describe:
"""
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pandas as pd
import codecs
import json

from settings import *

file_path_origin = os.path.join(conf.basic_path, conf.file_origin_kb)
df = pd.read_csv(file_path_origin, encoding='utf-8')

# [问题id]
# 根据【问题id】去重
df_dup_q = df.drop_duplicates(subset=[r'问题ID'])
print('==== 【{0}】 ===='.format(r'问题去重'))
print('去重前shape: {0}'.format(str(df.shape)))
print('去重后shape: {0}'.format(str(df_dup_q.shape)))
print('id重复: {0}  {1}'.format(df.shape[0]-df_dup_q.shape[0],(df.shape[0]-df_dup_q.shape[0])/df_dup_q.shape[0]))


question_unique = df_dup_q[[r'问题ID', r'问题名称']].values.tolist()
question_unique_content = {'data': question_unique}
file_path_question_unique = os.path.join(conf.basic_path, conf.file_question_unique)
with codecs.open(file_path_question_unique, 'w', 'utf-8') as f:
    json.dump(question_unique_content, f)

# [答案id]
# 根据【答案id】去重
df_dup_a = df.drop_duplicates(subset=[r'回答ID'])
print('==== 【{0}】 ===='.format(r'答案去重'))
print('去重前shape: {0}'.format(str(df.shape)))
print('去重后shape: {0}'.format(str(df_dup_a.shape)))
print('id重复: {0}  {1}'.format(df.shape[0]-df_dup_a.shape[0],(df.shape[0]-df_dup_a.shape[0])/df_dup_a.shape[0]))

answer_unique = df_dup_a[[r'回答ID', r'回答']].values.tolist()
answer_unique_content = {'data': answer_unique}
file_path_answer_unique = os.path.join(conf.basic_path, conf.file_answer_unique)
with codecs.open(file_path_answer_unique, 'w', 'utf-8') as f:
    json.dump(answer_unique_content, f)