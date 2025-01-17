# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""

import time
import itertools
from functools import cache

class Design:
    def __init__(self, patterns, design):
        self.patterns = set(patterns)
        self.design = design
        self.count = 0
        
    @cache
    def is_possible_count(self,design):
        if design == '':
            return 1
        
        count = 0
        for towel in self.patterns:
            # print(design, towel)
            if design.startswith(towel):
                 count += self.is_possible_count(design[len(towel):])
                 
        return count
    
    # @cache
    def is_possible(self,design):
        for towel in self.patterns:
            print(design, towel)
            if design.startswith(towel):
                 if self.is_possible(design[len(towel):]):
                     return True
            if design == '':
                return True
        return False
        
    def solve(self):
        return self.is_possible(self.design)

class Day19:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n\n')
        patterns = data_raw[0].split(', ')
        designs = data_raw[1].split('\n')         
        file.close()

        return patterns.copy(), designs.copy()

    def part1(self):
        patterns, designs = self.load_text(self.file_name)
        print(patterns,'\n',designs)
        ans = 0
        
        # towel = Design(patterns, designs[5])
        # print(towel.solve())
        
        
        for design in designs:
            towel = Design(patterns, design)
            if towel.is_possible(design):
                print(f'{design} : possible')
                ans += 1
            else:
                print(f'{design} : impossible')
        
        # ans = -1
        print(f'Answer part 1 is : {ans}')
        
    def part2(self):
        patterns, designs = self.load_text(self.file_name)
        print(patterns,'\n',designs)
        ans = 0
       
        for design in designs:
            towel = Design(patterns, design)
            ans += towel.is_possible_count(design)
            print(ans)
        
        print(f'Answer part 2 is : {ans}')


if __name__ == "__main__":
    file_name = 'input/input_day19.txt'
    # file_name = 'input/input_day19_example.txt'

    app = Day19(file_name)
    start = time.time()
    # app.part1()
    end = time.time()
    print(f'\nevaluation time part 1 and 2 : {end - start} sec')

    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')
