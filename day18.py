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
import heapq


class Ram:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.print_map()
        self.find_start_end()
        # self.exp = {'loc' = [],'dist_start': [], ''}
        # self.set_open = []
        # self.set_closed = []
        self.map_visit = self.map.copy()
        self.start_dir = (0, 1)
        self.count_loc()

        self.dir_all = ((0, 1), (0, -1), (1, 0), (-1, 0))

        self.set_open = []
        self.set_closed = []

    def load_map(self, data_input):
        n = max(max(data_input))
        
        self.map = np.full((n+1,n+1),'.')
        for ele in data_input:
            self.map[ele] = '#'        # self.map = data_input

    def print_map(self):
        print(self.map)

    def count_loc(self):
        self.total_locs = len(np.where(self.map == '.')[0])
        print('total locs : ',self.total_locs)

    def find_start_end(self):
        self.loc_start = (0,0)
        self.loc_end =(self.map.shape[0]-1,self.map.shape[1]-1)

        return (self.loc_start, self.loc_end)

    def get_lowest_h(self):
        lowest_h = float('inf')
        for node in self.set_open:
            if node.h_score < lowest_h:
                lowest_node = node
                lowest_h = node.h_score
        return lowest_node

    def get_lowest_f(self, fin_score):
        while self.set_open:
            node = heapq.heappop(self.set_open)
            self.remove_set(self.set_closed, node)
            score = node[4]
            if score > fin_score:
                self.add_set(self.set_closed, node)
                continue
            return node
        return None

    def check_for_equal(self, node, check_list):
        found = {t for t in check_list if t[1] == node[1]}
        if len(found) == 0:
            return False, node

        return True, found

    def add_neigbors(self, neighbor_nodes):
        for node in neighbor_nodes:
            check, nodes_repeated = self.check_for_equal(node, self.set_open)
            if check:
                for node_repeat in nodes_repeated:
                    if (node_repeat[4] > node[4]):
                        self.remove_set(self.set_open, node_repeat)
                        self.add_set(self.set_open, node)
                    elif (node_repeat[4] == node[4]) and False:
                        self.remove_set(self.set_open, node_repeat)
                        self.add_set(self.set_closed, node_repeat)
                        path = ()
                        node = list(node)
                        for step in node_repeat[5]:
                            if step not in node[5]:
                                node[5] += (step,)
                        self.add_set(self.set_open, tuple(node))
            elif not check:
                self.add_set(self.set_open, node)

    def dist_end(self, loc):
        return np.sqrt((loc[0]-self.loc_end[0])**2 + (loc[1]-self.loc_end[1])**2)

    def add_set(self, set_in, node):
        heapq.heappush(set_in, node)

    def remove_set(self, set_in, node):
        set_in.remove(node)

    def get_next(self, node):
        fact = 1
        loc = node[1]
        direc = node[2]
        h_score = node[4]
        neighbor_nodes = set()
        for direction in self.dir_all:
            loc_check = (loc[0]+direction[0], loc[1]+direction[1])

            if ((0 <= loc_check[0] <= self.map.shape[0] - 1) and
                    (0 <= loc_check[1] <= self.map.shape[1] - 1)): 
                loc_sign = self.map[loc_check]
                path = node[5]
                if loc_sign == '.' or loc_sign == 'E':
                    if (direc == direction):
                        f_score = h_score + 1 + self.dist_end(loc_check)*fact
                        path += ((loc_check),)
                        neighbor_nodes.add(
                            (f_score+1, loc_check, direction, self.loc_end, h_score+1, path))
                    elif (direc == (-direction[0], -direction[1])):
                        continue
                    else:
                        f_score = h_score + 1 + \
                            self.dist_end(loc_check)*fact
                        path += ((loc_check),)
                        neighbor_nodes.add(
                            (f_score, loc_check, direction, self.loc_end, h_score+1, path))
        return neighbor_nodes

    def remove_higher_than_x(self, heap, x):
        # Filter out elements greater than x
        filtered_heap = [item for item in heap if item[4] <= x]

        return filtered_heap

    def solve(self):
        loc_start, loc_end = self.find_start_end()
        low_score = float('inf')
        # start_node = Node(self.map,loc_start,self.start_dir,0,loc_end)
        path = ()
        path += ((loc_start,))
        start_node = (0, loc_start, self.start_dir, loc_end, 0, path)
        self.add_set(self.set_open, start_node)

        self.path_shortest = set()
        i = 0
        end_loop = 100000000
        while len(self.set_open) > 0 and i < end_loop:

            i += 1

            self.set_open = self.remove_higher_than_x(self.set_open, low_score)

            if len(self.set_open) == 0:
                return low_score

            current = self.get_lowest_f(low_score)

            print(f'\riterations : {i}, length open : {len(self.set_open)}, length closed : {
                  len(self.set_closed)}, pathlenght : {len(current[5])} ', end="\n")
            # print(current)
            if current is None:
                break

            neighbor_nodes = self.get_next(current)
            self.add_neigbors(neighbor_nodes)

            self.map_visit[current[1]] = '0'
            temp =  self.map_visit.copy()
            temp[current[1]] = 'X'
            # print(temp)


            if current[1][1] == self.loc_end[1] and current[1][0] == self.loc_end[0]:
                print('End Found')
                if low_score < current[0]:
                    self.path_shortest = set()
                self.finish_node = current

                self.path_shortest.add(current[5])
                low_score = current[0]

        return low_score


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
                line = line.split(',')
                data_output.append(tuple(map(int,line)))
        return data_output.copy()

    def part1_2(self):
        map_input = self.load_text(self.file_name)
        # ram = Ram(map_input[:1024])
        ram = Ram(map_input[:12])
        # self.ram = ram
        sol = ram.solve()
        
        finish_node = ram.finish_node
        finish_paths = finish_node[5]
        map_visited = ram.map
        
        for step in finish_paths:
            map_visited[step] = 'O'
            
        print(map_visited)
        
        
        ans = finish_node[4]
        print(f'Answer part 1 is : {ans}')


if __name__ == "__main__":
    plt.close('all')

    # file_name = 'input/input_day18.txt'
    file_name = 'input/input_day18_test.txt'
    # file_name = 'input/input_day18_test2.txt'

    app = Day16(file_name)
    start = time.time()
    app.part1_2()
    end = time.time()
    print(f'\nevaluation time part 1 and 2 : {end - start} sec')

    # start = time.time()
    # app.part2()
    # end = time.time()
    # print(f'evaluation time part 2 : {end - start} sec')
