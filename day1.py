# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:30:02 2024

@author: RobinMak
"""

import numpy as np


data = np.loadtxt('input/input_day1.txt')

#%%Part 1
list1 = np.sort(data[:,0])
list2 = np.sort(data[:,1])

dist_array = np.array([])
for i, ele in enumerate(list1):
    dist_inst = abs(list1[i]-list2[i])
    dist_array = np.append(dist_array,dist_inst)
    
answer = np.sum(dist_array)
print(int(answer))

#%% Part 2

simu_array = np.array([])
for i, ele in enumerate(list1):
    N = (np.count_nonzero(list2 == ele))
    
    simu_inst = N*ele
    simu_array = np.append(simu_array,simu_inst)
    
answer = np.sum(simu_array)
print(int(answer))