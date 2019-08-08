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


import numpy as np
a=[1,2,3]
b=[2,4,5]
c=[2,7,8]
d=[9,8,3]
x=np.vstack((a,b,c,d))


import pandas as pd
a = np.arange(1,13).reshape(6,2)
data =pd.DataFrame(a)
data.pct_change()

x.mean()
np.mean()

