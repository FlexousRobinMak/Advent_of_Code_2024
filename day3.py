# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import re
import numpy as np

class Day3:
    def __init__(self):
        self.file_name = ''
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
            

    def find_mul(self,str):
        # m = re.findall('mul(%s,%s)',str)
        patern = r'mul\(\d{1,3},\d{1,3}\)'
        m = re.findall(patern,str)
        return m
    
    def find_mul_do_dont(self,str):
        # m = re.findall('mul(%s,%s)',str)
        patern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
        m = re.findall(patern,str)
        return m
    
    def remove_mul_do_dont(self, str_array):
        new_array = []
        do_statement = True
        for ele in str_array:
            if ele == 'don\'t()':
                do_statement = False
            elif ele == 'do()':
                do_statement = True
                
            elif do_statement:
                new_array.append(ele)
            
        return new_array
    
    def load_text(self,file_name):
        file = open(file_name, "r")
        self.data = file.read()
        # self.data = np.loadtxt(file_name)
        return self.data
    
    def run_day3_part1(self):
        data = self.load_text(self.file_name)
        str_array = self.find_mul(data)
        answer = self.compute_mul(str_array)
        print(f'Answer day 3 Part 1: {answer}')
        
    def run_day3_part2(self):
        data = self.load_text(self.file_name)
        str_array = self.find_mul_do_dont(data)
        # print(str_array)
        str_array = self.remove_mul_do_dont(str_array)
        print(str_array)
        answer = self.compute_mul(str_array)

        # answer = self.compute_mul(str_array)
        print(f'Answer day 3 Part 2: {answer}')
        
if __name__ == "__main__":
    app = Day3()
    app.file_name = 'input/input_day3.txt' 
    app.run_day3_part1()
    app.run_day3_part2()
    data = app.data