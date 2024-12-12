# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import time 

class Stones:
    def __init__(self, input_data):
        self.input_seq = input_data
        self.known_dict = {}

    
    def blink(self,seq):
        new_seq = []
        for i,ele in enumerate(seq):
            # print('i : ', i , 'ele : ', ele)
            # print(ele)
            if ele in self.known_dict:
                # print(f' {ele} is known, is : {self.known_dict[ele]}')
                new_seq = self.add_dict_list(ele, new_seq)            
            else:
                new_val_seq = self.eval_val(ele,[]) 
                self.known_dict.update({ele:new_val_seq})
                new_seq = self.add_dict_list(ele, new_seq)        
                
        # self.known_dict ={}
        # print(self.known_dict)
        
        return new_seq

    def add_dict_list(self,ele,new_seq):
        for thing in self.known_dict[ele]:
            new_seq.append(thing)
            
        return new_seq

        
        
    def eval_val(self,ele, new_seq = []):
            # print(f'i : {i} , ele : {ele} , len seq : {len(seq)}')
        if ele == 0:
            new_seq.append(int(1))
        elif (len(str(ele)) % 2) == 0:
            i_mid = int(len(str(ele))/2)
            # print(f'len str : {len(str(ele))} , ele : {ele} , i : {i_mid}')
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
        # data = np.array([125])
        stones = Stones(data)
        start = time.time()

        seq = stones.blink_loop(data,35)
        # seq = stones.blink_loop([125,17],6)
        end = time.time()
        print(f'evaluation time : {end - start} sec')


        # print(seq)
        self.data = data
        self.stones = stones
        ans = len(seq)       
        print(f'Answer part 1 is : {ans}')

    def part2(self):

        
        ans = -1
        # print(f'Answer part 2 is : {ans}')



if __name__ == "__main__":
    file_name = 'input/input_day11.txt'
    # file_name = 'input/input_day11_test.txt'

    app = Day11(file_name)
    app.part1()
    # app.part2()
