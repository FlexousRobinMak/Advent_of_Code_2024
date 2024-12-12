# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import time 
import functools

class Stones:
    def __init__(self, input_data):
        self.input_seq = input_data
        self.known_dict = {}

    def blink(self,seq):
        new_seq = []
        for i,ele in enumerate(seq):
            temp_seq  = self.eval_val(ele)
            for ele_new in temp_seq:
                new_seq.append(ele_new)                
        return new_seq
       
    @functools.cache
    def eval_val(self, ele):
            # print(f'i : {i} , ele : {ele} , len seq : {len(seq)}')
            
        new_seq = []
        if ele == 0:
            new_seq.append(int(1))
        elif (len(str(ele)) % 2) == 0:
            i_mid = int(len(str(ele))/2)
            new_seq.append(int(str(ele)[:i_mid]))
            new_seq.append(int(str(ele)[i_mid:]))
        else:
            new_seq.append(ele*2024)
            
        return new_seq

    def blink_loop(self,seq,blinks):
        for i in range(blinks):
            print('iloop : ', i+1)
            seq = self.blink(seq)
        
        return seq

    @functools.cache
    def count_stones(self, ele,blinks):
            # print(f'i : {i} , ele : {ele} , len seq : {len(seq)}')
        if blinks == 0:
            return 1
        if ele == 0:
            return self.count_stones(1, blinks-1)
    
        if (len(str(ele)) % 2) == 0:
            i_mid = int(len(str(ele))/2)
            x1 = int(str(ele)[:i_mid])
            x2 = int(str(ele)[i_mid:])
            return self.count_stones(x1, blinks-1)+self.count_stones(x2, blinks-1)
        return self.count_stones(ele*2024, blinks-1)
        
            
    def blink_loop(self,seq,blinks):
        for i in range(blinks):
            print('iloop : ', i+1)
            seq = self.blink(seq)
        
        return seq
  

class Day11:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split(' ')
        file.close()
        data_output = []
        for line in data_raw:
            if len(line)>0:
                data_output.append(int(line))
        return (data_output)

    def part1(self):
        data = self.load_text(self.file_name)
        # print('raw : ', data)
        data = [125,17]
        stones = Stones(data)
        start = time.time()
        seq = [stones.blink_loop(s,3) for s in data]
        print(seq)
        # seq = stones.blink_loop(data,25)
        # seq = stones.blink_loop([125,17],6)
        end = time.time()
        print(f'evaluation time : {end - start} sec')

        # print(seq)
        # self.data = data
        # self.stones = stones
        ans = len(seq)       
        print(f'Answer part 1 is : {ans}')

    def part2(self):
        data = self.load_text(self.file_name)
        stones = Stones(data)

        ans1 = sum(stones.count_stones(s,25) for s in data)
        ans2 = sum(stones.count_stones(s,75) for s in data)
        # ans = -1
        print(f'Answer part 1 is : {ans1}')
        print(f'Answer part 2 is : {ans2}')



if __name__ == "__main__":
    file_name = 'input/input_day11.txt'
    # file_name = 'input/input_day11_test.txt'

    app = Day11(file_name)
    app.part1()
    # app.part2()
