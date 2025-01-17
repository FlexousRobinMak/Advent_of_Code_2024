# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
# import numpy as np
import time
# import re
# import matplotlib.pyplot as plt
# import scipy.stats as st
# import pandas as pd
# import heapq


class Robot:
    def __init__(self, map_input,moves_input):
        self.moves = moves_input
        self.load_map(map_input)
        self.print_map()
        self.loc = self.find_robot()
        self.dict_move = {
            '>'  : (0,1),
            '^'  : (-1,0),
            '<'  : (0,-1),
            'v'  : (1,0),
            }        
        
    def load_map(self, map_input):
        self.map = map_input

    def print_map(self):
        for line in self.map:
            print("".join(line))
        print('\n')
        
    def find_robot(self):
        loc = [(i,s.index('@')) for i, s in enumerate(self.map) if '@' in s]
        print(loc)
        return loc[0]
    
    def set_map(self, loc, char):
        self.map[loc[0]][loc[1]] = char
    
    def widen_map(self):
        new_map = []
        dict_widen = { 
            '#' : '##',
            'O' : '[]',
            '.' : '..',
            '@' : '@.'}
        for row_idx, row in enumerate(self.map):
            for col_idx, string in enumerate(row):
                new_char = dict_widen[self.map[row_idx][col_idx]]
                self.map[row_idx][col_idx] = new_char
            new_map.append(list(''.join(self.map[row_idx])))
            
        self.map = new_map
        self.loc = self.find_robot()

    def add_locs(self,loc1: tuple, loc2: tuple) -> tuple:
        return tuple(map(lambda x, y: x + y, loc1, loc2))
    
    def get_score(self):
        boxes = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(self.map)
            for col_idx, string in enumerate(row)
            for char_idx, char in enumerate(string)
            if char == 'O'
        ]        
        score = 0        
        for box in boxes:
            score += box[0]*100 + box[1]
        return score
    
    def move_robot(self,move: str):
        direction = self.dict_move[move]
        new_loc = self.add_locs(self.loc,direction)
        
        if self.map[new_loc[0]][new_loc[1]]  == '.':
            self.set_map(self.loc,'.')
            self.set_map(new_loc,'@')

            self.loc = new_loc
            
        elif self.map[new_loc[0]][new_loc[1]]  == 'O':
            self.move_box_small(self.loc, new_loc, direction)
            
        elif (self.map[new_loc[0]][new_loc[1]]  == '['  or  
              self.map[new_loc[0]][new_loc[1]]  == '[' ):
            self.move_box_wide(self.loc, new_loc, direction)

        elif self.map[new_loc[0]][new_loc[1]]  == '#':
            return
        
    def move_box_small(self, loc, first_box, direction):
        last_box = first_box
        while True:
            next_loc = self.add_locs(last_box,direction)
            if self.map[next_loc[0]][next_loc[1]]  == '.':
                self.set_map(self.loc,'.')
                self.set_map(first_box,'@')
                self.set_map(next_loc,'O')
                
                self.loc = first_box
                break

            elif self.map[next_loc[0]][next_loc[1]]  == '#':
                break
            
            last_box = next_loc
            
    def move_box_wide(self, loc, first_box, direction):
        last_box = first_box
        
        while True:
            next_loc = self.add_locs(last_box,direction)
            if self.map[next_loc[0]][next_loc[1]]  == '.':
                open_loc = next_loc
                break

            elif self.map[next_loc[0]][next_loc[1]]  == '#':
                return
            
            
            last_box = next_loc
            last_box_char = self.map[next_loc[0]][next_loc[1]] 

        while True:
            next_loc = self.add_locs(last_box,direction)
            if self.map[next_loc[0]][next_loc[1]]:
                break
                
        self.set_map(self.loc,'.')
        self.set_map(first_box,'@')
        self.set_map(open_loc,)
        
        self.loc = first_box

                     
    def solve(self):
        for move in self.moves:
            self.move_robot(move)
            if True:
                print(f'Move {move}:')
                self.print_map()
         
        return self.get_score()


class Day15:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n\n')
        file.close()
        map_input = []
        moves_input = []
        map_raw = data_raw[0].split('\n')
        moves_input = data_raw[1].replace('\n','')
        
        for line in map_raw:
            if len(line) > 0:
                map_input.append(list(line))
                
        return map_input, moves_input

    def part1(self):
        map_input, moves_input= self.load_text(self.file_name)
        robot = Robot(map_input,moves_input)
        ans = robot.solve()
        print(f'Answer part 1 is : {ans}')
        
    def part2(self):
        map_input, moves_input= self.load_text(self.file_name)
        robot = Robot(map_input,moves_input)
        robot.widen_map()
        robot.print_map()
        ans = robot.solve()
        ans = -1
        print(f'Answer part 2 is : {ans}')

if __name__ == "__main__":

    file_name = 'input/input_day15.txt'
    file_name = 'input/input_day15_test.txt'
    file_name = 'input/input_day15_test2.txt'

    app = Day15(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'\nevaluation time part 1 and 2 : {end - start} sec')

    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')
