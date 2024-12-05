# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import re
import numpy as np
import math 

class Day4:
    def __init__(self):
        self.file_name = ''
        self.search_string = 'XMAS'
        pass
    
    def compute_mul(self,str_array):
        sum_all = 0
        for ele in str_array:
            patern = r'\d{1,3}'
            m = re.findall(patern,ele)
            x = int(m[0])
            y = int(m[1])
            ans = x*y
            sum_all = ans + sum_all
        return sum_all
            
    
    def load_text(self,file_name):
        file = open(file_name, "r")
        self.data = file.read()
        return self.data
                                    
    def find_letter(self,str_arr,pattern):
        coordinates = []
        for row_idx, row in enumerate(str_arr):
            for match in re.finditer(pattern, row):
                col_idx = match.start()
                coordinates.append((row_idx, col_idx))
        return coordinates
                            
    def find_xmas(self,str_arr):
        dim_row = len(str_arr)
        dim_col = len(str_arr[0])
        Xmas_count = 0
        print(f'dimensions: ({dim_row},{dim_col})')
        letter_count = 0
        word = 'XMAS'
        X_locs = self.find_letter(str_arr,word[0])
        M_locs = self.find_letter(str_arr,word[1])
                
        for X_pos in X_locs:
            for M_pos in M_locs:
                dist = np.sqrt((X_pos[0]-M_pos[0])**2+(X_pos[1]-M_pos[1])**2)
                if dist <= np.sqrt(2):
                    # print(f'X_pos = { X_pos}')
                    # print(f'M_pos = { M_pos}')


                    row_dir = M_pos[0]-X_pos[0]
                    col_dir = M_pos[1]-X_pos[1]
                    # print(f'dir({row_dir},{col_dir})')
                    
                    Pos_last = M_pos                    
                    for letter in word[2:]:
                        row_loc_next = Pos_last[0]+row_dir
                        col_loc_next = Pos_last[1]+col_dir
                        
                        if 0 <= row_loc_next <= dim_row-1 and 0 <= col_loc_next <= dim_col-1:
                            next_str = str_arr[row_loc_next][col_loc_next]
                            if next_str == letter:
                                Pos_last= [row_loc_next,col_loc_next]
                                # print(next_str)
                                if letter == 'S':
                                    Xmas_count += 1
                                    print(Xmas_count)
                            else:
                                break
        return Xmas_count
    
    def find_x_mas(self,str_arr):
        dim_row = len(str_arr)
        dim_col = len(str_arr[0])
        Xmas_count = 0
        print(f'dimensions: ({dim_row},{dim_col})')
        letter_count = 0
        word = 'XMAS'
        A_locs = self.find_letter(str_arr,'A')
        M_locs = self.find_letter(str_arr,'M')
                
        for A_pos in A_locs:
            for M_pos in M_locs:
                dist = np.sqrt((A_pos[0]-M_pos[0])**2+(A_pos[1]-M_pos[1])**2)
                if dist == np.sqrt(2):
                    print(f'A_pos = { A_pos}')
                    print(f'M_pos = { M_pos}')


                    row_dir = M_pos[0]-A_pos[0]
                    col_dir = M_pos[1]-A_pos[1]
                    # print(f'dir({row_dir},{col_dir})')
                    
                    
                    for letter in ['MSS']:
                        row_loc_next = A_pos[0]+row_dir
                        col_loc_next = A_pos[1]+col_dir
                        
                        if 0 <= row_loc_next <= dim_row-1 and 0 <= col_loc_next <= dim_col-1:
                            next_str = str_arr[row_loc_next][col_loc_next]
                            if next_str == letter:
                                Pos_last= [row_loc_next,col_loc_next]
                                # print(next_str)
                                if letter == 'S':
                                    Xmas_count += 1
                                    print(Xmas_count)
                            else:
                                break
        return Xmas_count
    
    def load_text(self,file_name):
        file = open(file_name, "r")
        self.data = np.array(file.read().split('\n'))
        # self.data = np.loadtxt(file_name)
        return self.data
    
    def run_day4_part1(self):
        self.data = self.load_text(self.file_name)
        answer = self.find_xmas(self.data)
        print(f' answer is : {answer}')

    def run_day4_part2(self):
        self.data = self.load_text(self.file_name)
        answer = self.find_x_mas(self.data)
        print(f' answer is : {answer}')
        # self.find_xmas(self.data)
        
if __name__ == "__main__":
    app = Day4()
    app.file_name = 'input/input_day4.txt' 
    app.file_name = 'input/input_day4_test.txt' 
    # app.run_day4_part1()
    app.run_day4_part2()
    data = app.data