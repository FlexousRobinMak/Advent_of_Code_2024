# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import re
import numpy as np
import math 

class Day5:
    def __init__(self):
        self.file_name = ''
        pass

    def load_text(self,file_name):
        file = open(file_name, "r")
        data = np.array(file.read().split('\n\n'))
        return data
                                    
    def get_rules(self,data):
        rules_raw = data[0].split('\n')
        rules_array = []
        for rule in rules_raw:
            rule_split = rule.split('|')
            rule_int = list(map(int, rule_split))
            rules_array.append(rule_int)
        return rules_array    
    
    def get_lines(self,data):
        lines = data[1].split('\n')
        line_array = []
        for line in lines:
            line_split = line.split(',')            
            line_int = list(map(int, line_split))
            line_array.append(line_int)
        return line_array
    
    def check_line(self,line, rules):
        state = True
        for rule in rules:
            idx_1 = self.find_index(line,rule[0])
            idx_2 = self.find_index(line,rule[1])
            if idx_1 < 0 or idx_2 < 0 or idx_1 < idx_2 : 
                continue 
            else:
                state = False
        return state 
    
    def correct_line(self,line, rules):
        state = True
        new_line = line
        for rule in rules:
            idx_1 = self.find_index(new_line,rule[0])
            idx_2 = self.find_index(new_line,rule[1])
            if idx_1 < 0 or idx_2 < 0:
                continue
            elif idx_1 > idx_2 : 
                new_line = self.move2idx(new_line, idx_2, idx_1)
            else:
                continue
        return new_line 
    
    def move2idx(self,arr,idx_start,idx_end):
        num = arr[idx_start]
        arr.pop(idx_start)
        arr.insert(idx_end,num)
        return arr
    
    def check_all_lines(self,lines,rules):
        arr_correct = []
        arr_incorrect = []
        for line in lines:
            line_check = self.check_line(line,rules)
            if line_check:
                arr_correct.append(line)
            else: 
                arr_incorrect.append(line)
        return arr_correct, arr_incorrect
            
    def correct_all_lines(self,lines,rules):
        arr_corrected = []
        for line in lines:
            corrected_line = self.correct_line(line,rules)
            arr_corrected.append(corrected_line)
        return arr_corrected
    
    def find_index(self,arr,num):
        try:
            index = arr.index(num)
            return index
        except ValueError:
            return -1
    
    def add_middle_values(self, lines):
        sum_mid = 0
        for line in lines:
            mid_idx = len(line)//2
            mid_num = line[mid_idx]
            sum_mid +=  mid_num
        return sum_mid
            
    def run_day5_part1(self):
        data = self.load_text(self.file_name)
        rules = self.get_rules(data)
        lines = self.get_lines(data)
        correct_lines, X = self.check_all_lines(lines,rules)
        answer = self.add_middle_values(correct_lines)

        print(f' answer part 1 is : {answer}')

    def run_day5_part2(self):
        data = self.load_text(self.file_name)
        rules = self.get_rules(data)
        lines = self.get_lines(data)
        line_test = []
        for i in range(1,100):
            line_test.append(i)
        lines = line_test
        print(lines)
        X, incorrect_lines = self.check_all_lines(lines,rules)
        corrected_lines = self.correct_all_lines(incorrect_lines, rules)
        i=0
        last_list = []
        while True:
            i+=1
            X, incorrect_lines_check = self.check_all_lines(corrected_lines, rules)
            if len(incorrect_lines_check) == 0:
                break
            elif i > 100:
                print("not found")
                break
            print(i)
            
            corrected_lines = self.correct_all_lines(corrected_lines, rules)


                
        answer = self.add_middle_values(incorrect_lines)

        print(f' answer part 2 is : {answer}')
        
if __name__ == "__main__":
    app = Day5()
    app.file_name = 'input/input_day5.txt' 
    # app.file_name = 'input/input_day5_test.txt' 
    app.run_day5_part1()
    app.run_day5_part2()

    # print(rules)
    # print(lines)
