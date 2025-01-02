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

class Reindeer:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.find_start_end()
        # self.exp = {'loc' = [],'dist_start': [], ''}
        self.set_open = []
        self.set_closed = []
        self.map_visit = self.map.copy()
        self.start_dir = np.array([0,1])
        self.count_loc()

        
    def load_map(self, data_input):
        self.map = data_input

    def print_map(self):
        print(self.map)

    def count_loc(self):
        self.total_locs = len( np.where(self.map == '.')[0])
        print(self.total_locs)
        
    def find_start_end(self):
        loc_start = np.where(self.map == 'S')
        loc_end = np.where(self.map == 'E')
        
        self.loc_start = [loc_start[0][0],loc_start[1][0]]
        self.loc_end = [loc_end[0][0],loc_end[1][0]]
        return self.loc_start, self.loc_end 
    
    def get_lowest_h(self):
        lowest_h = float('inf')            
        for node in self.set_open:
            if node.h_score <= lowest_h:
                lowest_node = node
                lowest_h = node.h_score
        return lowest_node

    def get_lowest_f(self,fin_score):
        lowest_score = float('inf')     
        lowest_node = None
        for node in self.set_open:
            score = node.get_f_score()
            if score >= fin_score:
                self.set_open.remove(node)
                self.set_closed.append(node)
                continue 
            
            if score <= lowest_score :
                lowest_node = node
                lowest_score = score
                
        return lowest_node
                
    def check_in_list(self,node,check_list):
        for check_node in check_list:
            if (check_node.loc == node.loc).all():
                if (check_node.dir == node.dir).all() or (check_node.dir == -1*node.dir).all():
                    return True, check_node

        return False, node
    
    def add_neigbors(self,neighbor_nodes):
        for node in neighbor_nodes:
            check, node_repeat = self.check_in_list(node, self.set_open)
            if check:
                if (node_repeat.h_score > node.h_score):        
                    node_repeat.h_score = node.h_score
                    node_repeat.dir = node.dir
            elif not check:
                self.set_open.append(node)
            
    def solve(self):
        loc_start,loc_end = self.find_start_end()
        low_score = float('inf')
        start_node = Node(self.map,loc_start,self.start_dir,0,loc_end)
        self.set_open.append(start_node)
        
        i = 0
        end_loop = 1000000
        while len(self.set_open) > 0 and i < end_loop:
            
            i += 1
            print(f'\riterations : {i}, length open : {len(self.set_open)}, length closed : {len(self.set_closed)} ', end="")
            # print('len : ', len(self.set_open))
            current = self.get_lowest_f(low_score)
            
            if current is None:
                break
            
            self.set_open.remove(current)
            self.set_closed.append(current)
            
            self.map_visit[current.row,current.col] = '0'
            temp =  self.map_visit.copy()
            temp[current.row,current.col] = 'X'
            # print(temp)
            neighbor_nodes = current.get_next()
            self.add_neigbors(neighbor_nodes)

            if self.map[current.row,current.col] == 'E':
                low_score = current.h_score
                print(low_score)

        return low_score
            

class Node:
    def __init__(self, map_in , loc_in, dir_in, h, loc_end):
        self.loc = loc_in
        self.loc_end = loc_end
        self.dir = dir_in
        self.row = self.loc[0]
        self.col = self.loc[1]
        self.map = map_in
        self.g_score = self.dist_end(self.loc)
        self.h_score = h
        
        
    def get_next(self):
        dir_all = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        neighbor_nodes = []
        for direction in dir_all:
            loc_check = self.loc+direction
            loc_sign = self.map[loc_check[0],loc_check[1]]
            if ((0 <= loc_check[0] <= self.map.shape[0] - 1) and 
                (0 <= loc_check[1] <= self.map.shape[1] - 1)):
                if loc_sign == '.' or loc_sign == 'E':
                    if (self.dir == direction).all(): 
                        neighbor_nodes.append(Node(self.map,loc_check,direction,self.h_score+1,self.loc_end))
                    elif (self.dir == direction*-1).all():
                         continue  
                    else:
                        neighbor_nodes.append(Node(self.map,loc_check,direction,self.h_score+1001,self.loc_end))
        return neighbor_nodes
    
    def dist_end(self,loc):
        return np.sqrt((loc[0]-self.loc_end[0])**2 + (loc[1]-self.loc_end[1])**2)
    
    def get_f_score(self):
        return self.h_score + self.g_score*1
        
    
class Day16:
    def __init__(self, file_name_input):
        self.file_name = file_name_input
        

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')
        file.close()
        data_output = []
        for line in data_raw:
            if len(line) > 0:
                data_output.append(list(line))
        return np.array(data_output)

    def part1(self):
        map_input = self.load_text(self.file_name)
        reindeer = Reindeer(map_input)
        # reindeer.print_map()
        x = reindeer.solve()
        
        # print(x)
        ans = x
        print(f'Answer part 1 is : {ans}')

        

    def part2(self):
        data = self.load_text(self.file_name)
        ans = -1
        print(f'Answer part 2 is : {ans}')


if __name__ == "__main__":
    plt.close('all')

    file_name = 'input/input_day16.txt'
    file_name = 'input/input_day16_test.txt'
    # file_name = 'input/input_day16_test2.txt'
    # file_name = 'input/input_day16_test3.txt'
    # file_name = 'input/input_day16_test4.txt'
    # 
    app = Day16(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'\nevaluation time part 1 : {end - start} sec')
    
    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')