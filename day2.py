# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:30:02 2024

@author: RobinMak
"""

import numpy as np
import pandas as pd

# data = pd.read_csv('input/input_day2.txt', header=None)
data = pd.read_csv('input/data_JM.txt', header=None)
# data = data[0].str.split('\s\|\s', expand=True)


safe_count_all = 0
for i, row in data.iterrows():
    row = np.array(row.values[0].split())
    row = np.asarray(row, dtype=int)
    safe_count = 0
    for i_rem, ele in enumerate(row):
        row_temp = np.delete(row,i_rem)
        diff = np.diff(row_temp)
        if diff[0] > 0:
            if max(diff) <= 3 and min(diff) >=1 :
                safe_count = safe_count +1
        elif diff[0] < 0:
            if min(diff) >= -3 and max(diff) <= -1 :
                safe_count = safe_count +1
    if safe_count > 0:
        safe_count_all = safe_count_all +1
            
print(safe_count_all)
