# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import time

class Garden:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.dir_all = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        # self.plot_temp = np.array([]).astype(np.int64)
        self.plot_temp = []
        self.plots = []
        self.perim_temp = 0
        self.perim = []
        self.price = []
        self.search_map = np.full(self.map.shape, False)

    def load_map(self, data_input):
        self.map = data_input

    def print_map(self):
        print(self.map)

    def get_all_plots(self):
        plots = []
        for i_row in range(self.map.shape[0]):
            for i_col in range(self.map.shape[1]):
                plant = self.map[i_row, i_col]
                loc = [int(i_row), int(i_col)]
                if not self.search_map[loc[0], loc[1]]:
                    plot_res, perim_res  = self.explore_plot(plant, loc, [], 0)
                    # plot_res, perim_res  = self.explore_plot_old(plant, loc, [], 0)
                    # plot_res, perim_res  = self.explore_plot_new(plant, loc, [], 0)
                    print(plot_res,perim_res)
                    plots.append(plot_res)
                    self.perim.append(perim_res)
                    self.price.append(len(plot_res)*perim_res)
        return plots

    def explore_plot_new1(self, plant, loc, plot, perim):
        plot.append([loc[0], loc[1]])
        self.search_map[loc[0], loc[1]] = True
        perim += 4
        for dir_check in self.dir_all:
            next_loc = loc+dir_check
            loc_val = self.map[loc[0], loc[1]]
            if ((0 <= next_loc[0] <= self.map.shape[0] - 1) and
                    (0 <= next_loc[1] <= self.map.shape[1] - 1)):
                next_val = self.map[next_loc[0], next_loc[1]]
                if (next_val == plant):
                    perim += -1
                    if not self.search_map[next_loc[0], next_loc[1]]:
                        self.explore_plot(plant, next_loc,plot,perim)
        return plot, perim
    
    def explore_plot(self, plant, loc, plot, perim):
        self.plot_temp.append([loc[0], loc[1]])
        self.search_map[loc[0], loc[1]] = True
        self.perim_temp += 4
        for dir_check in self.dir_all:
            next_loc = loc+dir_check
            loc_val = self.map[loc[0], loc[1]]
            if ((0 <= next_loc[0] <= self.map.shape[0] - 1) and
                    (0 <= next_loc[1] <= self.map.shape[1] - 1)):
                next_val = self.map[next_loc[0], next_loc[1]]
                if (next_val == plant):
                    self.perim_temp += -1
                    if not self.search_map[next_loc[0], next_loc[1]]:
                        self.explore_plot(plant, next_loc,[],0)
        return self.plot_temp, self.perim_temp
    
    def explore_plot_new2(self, plant, loc, plot, perim):
        plot.append([loc[0], loc[1]])
        self.search_map[loc[0], loc[1]] = True
        perim += 4
        for dir_check in self.dir_all:
            next_loc = loc+dir_check
            loc_val = self.map[loc[0], loc[1]]
            if ((0 <= next_loc[0] <= self.map.shape[0] - 1) and
                    (0 <= next_loc[1] <= self.map.shape[1] - 1)):
                next_val = self.map[next_loc[0], next_loc[1]]
                if (next_val == plant):
                    perim += -1
                    if not self.search_map[next_loc[0], next_loc[1]]:
                        self.explore_plot_new(plant, next_loc,plot,perim)
        return plot, perim


class Day12:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read().split('\n')
        file.close()
        data_output = []
        for line in data_raw:
            if len(line) > 0:
                data_output.append(list(line))
        return np.array(data_output)

    def part1(self):
        data = self.load_text(self.file_name)
        garden = Garden(data)
        # garden.print_map()
        plots = garden.get_all_plots()

        ans = np.sum(garden.price)
        print(f'Answer part 1 is : {ans}')
        

    def part2(self):
        data = self.load_text(self.file_name)
        ans = -1
        print(f'Answer part 2 is : {ans}')


if __name__ == "__main__":
    file_name = 'input/input_day12.txt'
    # file_name = 'input/input_day12_test.txt'
    # file_name = 'input/input_day12_test2.txt'

    app = Day12(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'evaluation time part 1 : {end - start} sec')
    
    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')