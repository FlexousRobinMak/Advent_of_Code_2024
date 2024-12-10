# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np

class TopoMap:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.dir_all = np.array([[0,1],[0,-1],[1,0],[-1,0]])
        self.opt_temp = np.array([])

    def load_map(self, data_input):
        self.map = data_input

    def print_map(self):
        print(self.map)

    def find_start(self):
        loc_start = list(np.where(self.map == 0))
        return np.array(loc_start)
    
    def find_end(self):
        loc_end = np.where(self.map == 9)
        return loc_end

    def get_possible_opt(self,start):
        if len(self.opt_temp) <= 0:
            loc_val = self.map[start[0],start[1]]
            self.opt_temp = np.array([loc_val,start[0],start[1]])
            
        opt_next = self.check_next(start)
        for ele in opt_next:
            self.get_possible_opt(ele)
            
        return self.opt_temp
        	
    def check_next(self,loc):
        opt_next = []
        for dir_check in self.dir_all:
            next_loc = loc+dir_check
            loc_val = self.map[loc[0],loc[1]]
            if  (( 0 <= next_loc[0] <= self.map.shape[0] - 1) and
                 ( 0 <= next_loc[1] <= self.map.shape[1] - 1) ):
                next_val = self.map[next_loc[0],next_loc[1]]
                
                if (loc_val == next_val-1): 
                    # print(f'loc : {loc}, loc_val : {loc_val} || next_loc : {next_loc}, next_val : {next_val}')
                    opt_next.append(next_loc)
                    self.opt_temp = np.vstack((self.opt_temp,[next_val ,next_loc[0],next_loc[1]]))
        return opt_next            
    
    def get_sol(self):
        start_pos = self.find_start()
        count_route = 0
        ans = []
        for i,ele in enumerate(start_pos[0]):
        # i = 0
            start = np.array([start_pos[0][i],start_pos[1][i]])
            self.get_possible_opt(start)
            
            sol_unique = np.unique(self.opt_temp , axis=0)
            sol = self.opt_temp

            unique, counts = np.unique(sol_unique[:,0], return_counts=True)
            sol_count_unique = dict(zip(unique, counts))
            ans.append(sol_count_unique[9])

            unique, counts = np.unique(sol[:,0], return_counts=True)
            sol_count = dict(zip(unique, counts))
            count_route += sol_count[9]
            
            self.opt_temp = np.array([])
            
        return ans, count_route
  

class Day10:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')
        file.close()
        data_output = []
        for line in data_raw:
            if len(line)>0:
                data_output.append(list(line))
        return np.array(data_output).astype(int)

    def part1(self):
        data = self.load_text(self.file_name)
        
        topomap = TopoMap(data)
        self.x = topomap
        ans, count = topomap.get_sol()

        ans = np.sum(ans)
        print(f'Answer part 1 is : {ans}')
        print(f'Answer part 2 is : {count}')

    def part2(self):

        ans = -1
        # print(f'Answer part 2 is : {ans}')


if __name__ == "__main__":
    file_name = 'input/input_day10.txt'
    # file_name = 'input/input_day10_test.txt'

    app = Day10(file_name)
    app.part1()
    app.part2()
