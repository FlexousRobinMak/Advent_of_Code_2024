# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import itertools


class Day7:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')

        return data_raw

    def split_text(self, data_input):
        arr_req_ans = []
        arr_numbers = []
        for line in data_input:
            line_split = line.split(': ')
            req_ans = int(line_split[0])
            numbers_str = line_split[1].split(' ')
            numbers = [int(item) for item in numbers_str]
            arr_req_ans.append(req_ans)
            arr_numbers.append(numbers)
        return arr_req_ans, arr_numbers

    def solve_eq_old(self, numbers_in, operators):
        operators = list(operators)
        
        numbers_new = np.array(numbers_in)

        while True:
            indices = [i for i, x in enumerate(operators) if x == "|"]
            if len(indices) < 1:
                break
            else:
                print(numbers_new)
                i = indices[0]
                numbers_new[i] = int(str(numbers_new[i])+str(numbers_new[i+1]))
                numbers_new = np.delete(numbers_new, i+1)
                del operators[i]
        print(numbers_new)
        
        sol_temp = numbers_new[0]
        for i, num in enumerate(numbers_new[1:]):
            if operators[i] == '+':
                sol_temp = sol_temp + num
            elif operators[i] == 'X':
                sol_temp = sol_temp * num

        return sol_temp
        
    
    def solve_eq(self, ans,  numbers_in, operators):
        operators = list(operators)
        
        numbers_new = np.array(numbers_in)
        
        sol_temp = numbers_new[0]
        for i, num in enumerate(numbers_new[1:]):
            # if sol_temp >= ans:
            #     return -1
            
            if operators[i] == '+':
                sol_temp = sol_temp + num
            elif operators[i] == 'X':
                sol_temp = sol_temp * num
            elif operators[i] == '|':
                sol_temp = int(str(sol_temp)+str(num))
                
        return sol_temp
        

    def get_operators(self, ans, numbers_in, operators):
        sol_operators = []
        perm_list = list(itertools.product(operators, repeat=len(numbers_in)-1))
                
        numbers = numbers_in

        for operator in perm_list:
            numbers = numbers_in
            sol = self.solve_eq(ans,numbers, operator)
            # print(f'op: {operator}, num: {numbers}, ans : {ans}, sol : {sol}' )
            if sol == ans:
                sol_operators.append(operator)

        return sol_operators

    def part1(self):
        data = self.load_text(self.file_name)
        list_ans, list_num = self.split_text(data)
        self.max_ans = max(list_ans)

        operators = 'X+'
            
        ans_sum = 0
        for i in range(len(list_ans)):
            sol = self.get_operators(list_ans[i], list_num[i], operators)
            if len(sol) > 0:
                ans_sum += list_ans[i]
        print(f'Answer part 1 is : {ans_sum}')

    def part2(self):
        
        data = self.load_text(self.file_name)
        list_ans, list_num = self.split_text(data)  
        operators = '+*|'
        self.max_ans = max(list_ans)

        ans_sum = 0
        for i in range(len(list_ans)):
            print(f"\rProgress : {i+1}/{len(list_ans)} {round((i+1)/len(list_ans)*100,2)}% ", end="")
            
            sol = self.get_operators(list_ans[i], list_num[i], operators)
            if len(sol) > 0:
                ans_sum += list_ans[i]
                
        print('')
        print(f'Answer part 2 is : {ans_sum}')

if __name__ == "__main__":
    file_name = 'input/input_day7.txt'
    # file_name = 'input/input_day7_test.txt'

    app = Day7(file_name)
    app.part1()
    # app.part2()
