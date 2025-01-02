# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import time
import re
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd

class Robot:
    def __init__(self, p_start ,v_start , settings):
        # self.load_map(input_data)
        self.p = p_start
        self.v = v_start
        self.steps = 0
        
        self.map_size = settings['map_size']
        self.max_steps = settings['max_steps']
        
    def load_map(self, data_input):
        self.map = data_input

    def print_map(self):
        print(self.map)
        
    def get_quadrant(self,p,v,dx):
        p_end = self.move(p,v,dx,0)
        q = [[0, 0], [0, 0]]
        # print(p_end)
        if p_end[0] < (self.map_size[0]-1)/2:
            i = 0 
        elif p_end[0] > (self.map_size[0]-1)/2:
            i = 1            
        else: 
            return q,p_end
        
        if p_end[1] < (self.map_size[1]-1)/2:
            q[0][i] = 1
        elif p_end[1] > (self.map_size[1]-1)/2:
            q[1][i] = 1
        else:
            return q,p_end
        
        return q,p_end
    
    def move(self,p,v,dx, steps):

        x_new = (p[0] + v[0]*dx) % self.map_size[0]
        y_new = (p[1] + v[1]*dx) % self.map_size[1]
        p_new = [x_new, y_new]
        
        steps += dx
        if steps >= self.max_steps:
            return p_new
        else:
            return self.move(p_new, v, dx, steps)



class Day12:
    def __init__(self, file_name_input):
        self.file_name = file_name_input
        
    def get_num(self,str_in):
        pattern = r'[+-]?\d+'
        m = re.findall(pattern,str_in)
        m_new = [int(item) for item in m]
        return m_new

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')
        file.close()
        p = []
        v = []
        for line in data_raw:
            if len(line) > 0:
                m = self.get_num(line)
                p.append([m[0],m[1]])
                v.append([m[2],m[3]])
        return p,v

    def part1(self):
        p, v = self.load_text(self.file_name)
        settings = {}
        # settings['map_size'] = [11,7]
        settings['map_size'] = [101,103]
        center = (np.array(settings['map_size'])-1)/2
        q = [[0, 0], [0, 0]]
        
        results = pd.DataFrame(columns=['mean_dist', 'p_all_np'])
        p_all_list = []
        mean_dist_list = []

        loop_length = 10
        for steps in range(loop_length):
            
            print(f"\rProgress : {steps+1}/{loop_length} {round((steps+1)/(loop_length)*100, 2)}% ", end="")
            
            settings['max_steps'] = steps
            p_all = []

            for i,ele in enumerate(p):
                robot = Robot(p[i],v[i],settings)
                q_new,p_end = robot.get_quadrant(p[i],v[i],steps)
                q = [[q[i][j] + q_new[i][j] for j in range(2)] for i in range(2)]
                p_all.append(p_end)
                
                
            p_all_np = np.array(p_all)
            x = p_all_np[:,0]
            y = p_all_np[:,1]
            
            p_all_list.append()
                        
            dist = np.sqrt((p_all_np[:,0]-center[0])**2+(p_all_np[:,1]-center[1])**2)
            mean_dist = np.mean(dist)
            # print(mean_dist)


            # results[steps]= {
            #     'mean_dist' : mean_dist, 
            #     'p_all_np' : p_all_np} 

            if False:
                plt.figure(steps, figsize=(5,5))
                plt.scatter(x[:,0],x[:,1])
                plt.show()
                
                
    
        # res = pd.DataFrame(results)

        # res = res.sort_values(by='mean_dist')

        self.res = res
        ans = q[1][1]*q[1][0]*q[0][0]*q[0][1]
        print(f'Answer part 1 is : {ans}')
        q = []
            # map = np.fill('.',)
        

    def part2(self):
        data = self.load_text(self.file_name)
        ans = -1
        print(f'Answer part 2 is : {ans}')


if __name__ == "__main__":
    plt.close('all')

    file_name = 'input/input_day14.txt'
    # file_name = 'input/input_day14_test.txt'
    
    app = Day12(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'evaluation time part 1 : {end - start} sec')
    
    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')