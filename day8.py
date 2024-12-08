# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import itertools


class City:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.node_map = np.full(self.city_map.shape, '.')
        self.repeat_sig = False
    def load_map(self, data_input):
        self.city_map = data_input

    def print_map(self):
        print(self.city_map)

    def get_antennas(self):
        ant, i_ant = np.unique(self.city_map, return_index=True)
        ant = ant[ant != '.']
        return ant

    def find_antennas(self, ant):
        loc_ant = np.where(self.city_map == ant)
        return loc_ant

    def get_node_loc_wrong(self, ant1, ant2):
        row_dist = ant2[0] - ant1[0]
        col_dist = ant2[1] - ant1[1]
        node_loc = []
        node_dist = np.array([row_dist, col_dist])

        if self.repeat_sig:
            loop_length = int(max(self.city_map.shape))
        else: 
            loop_length = 1
        
        for i in range(loop_length):     
            node_loc_temp = [ant1 - node_dist*i, ant2 + node_dist*i]
            for loc in node_loc_temp:
                if (0 <= loc[0] <= self.city_map.shape[0] - 1 and
                        0 <= loc[1] <= self.city_map.shape[1] - 1):
                        node_loc.append(loc)
                        
        return np.array(node_loc)
    
    def get_node_loc(self, ant1, ant2):
        row_dist = ant2[0] - ant1[0]
        col_dist = ant2[1] - ant1[1]

        node_dist = np.array([row_dist, col_dist])
        
        node_loc = []

        if self.repeat_sig:
            loop_length = int(max(self.city_map.shape)+1)
            loop_range = range(0,loop_length+1,1)
        else: 
            loop_range = range(1,1+1,1)
        
        for i in loop_range:     
            node_loc_temp = [ant1 - node_dist*i, ant2 + node_dist*i]
            for loc in node_loc_temp:
                if (0 <= loc[0] <= self.city_map.shape[0] - 1 and
                        0 <= loc[1] <= self.city_map.shape[1] - 1):
                    node_loc.append(loc)
        return np.array(node_loc)


    def get_node_loc_working (self, ant1, ant2):
        row_dist = ant2[0] - ant1[0]
        col_dist = ant2[1] - ant1[1]

        node_dist = np.array([row_dist, col_dist])
        node_loc_temp = [ant1 - node_dist, ant2 + node_dist]
        node_loc = []
        for loc in node_loc_temp:
            if (0 <= loc[0] <= self.city_map.shape[0] - 1 and
                    0 <= loc[1] <= self.city_map.shape[1] - 1):
                node_loc.append(loc)
        return np.array(node_loc)
    
    
    def find_nodes(self, ant, loc_ant):
        n_loc = len(loc_ant[0])
        comb_list = list(itertools.combinations(np.arange(0, n_loc, 1), 2))
        for comb in comb_list:
            ant1 = np.array([loc_ant[0][comb[0]], loc_ant[1][comb[0]]])
            ant2 = np.array([loc_ant[0][comb[1]], loc_ant[1][comb[1]]])
            node_loc = self.get_node_loc(ant1, ant2)
            self.store_nodes(node_loc)

    def count_nodes(self):
        loc_ant = np.where(self.node_map == '#')
        return len(loc_ant[0])

    def store_nodes(self, loc_nodes):
        if loc_nodes is not None:
            for loc in loc_nodes:
                self.node_map[loc[0]][loc[1]] = '#'

    def solve_city(self):
        antennas = self.get_antennas()
        for ant in antennas:
            loc_ant = self.find_antennas(ant)
            loc_nodes = self.find_nodes(ant, loc_ant)


class Day8:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')
        file.close()
        data_output = []
        for line in data_raw:
            data_output.append(list(line))
        return np.array(data_output)

    def part1(self):
        data = self.load_text(self.file_name)

        city = City(data)
        city.repeat_sig = False

        city.solve_city()
        answer = -1

        print(city.city_map)
        print(city.node_map)

        self.city = city

        answer = city.count_nodes()

        print(f'Answer part 1 is : {answer}')

    def part2(self):
        data = self.load_text(self.file_name)
        city = City(data)
        city.repeat_sig = True

        city.solve_city()
        answer = -1

        print(city.city_map)
        print(city.node_map)

        self.city = city

        answer = city.count_nodes()
        
        print(f'Answer part 2 is : {answer}')


if __name__ == "__main__":
    file_name = 'input/input_day8.txt'
    # file_name = 'input/input_day8_test.txt'

    app = Day8(file_name)
    app.part1()
    app.part2()
