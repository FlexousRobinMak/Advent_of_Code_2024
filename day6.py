# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np


class Guard:
    def __init__(self, input_data):
        self.loc = []
        self.direc = []
        self.direc_key = []

        self.guard_dirs = {
            '^': [-1, 0],
            '>': [0, 1],
            'v': [1, 0],
            '<': [0, -1]
        }

        self.load_map(input_data)
        self.visited_locations = np.zeros(
            [self.guard_map.shape[0], self.guard_map.shape[1]])
        self.get_loc()

    def load_map(self, data_input):
        self.guard_map = data_input

    def print_map(self):
        print(self.guard_map)

    def get_loc(self):
        for key in self.guard_dirs:
            loc_temp = np.where(self.guard_map == key)

            if np.any(loc_temp):
                break

        self.loc = np.array([loc_temp[0][0], loc_temp[1][0]])
        self.direc = np.array(self.guard_dirs[key])
        self.direc_key = np.array(key)

        return self.loc, self.direc, self.direc_key

    def check_next(self):
        stop_run = False
        idx_next_field = self.loc+self.direc
        if (0 <= idx_next_field[0] <= self.guard_map.shape[0] - 1 and
                0 <= idx_next_field[1] <= self.guard_map.shape[1] - 1):
            next_field = self.guard_map[idx_next_field[0], idx_next_field[1]]
        else:
            stop_run = True
            next_field = []

        return idx_next_field, next_field, stop_run

    def step_forward(self, next_idx):
        self.guard_map[next_idx[0], next_idx[1]] = self.direc_key
        self.guard_map[self.loc[0], self.loc[1]] = 'X'
        self.visited_locations[self.loc[0], self.loc[1]] += 1
        self.loc = [next_idx[0], next_idx[1]]

    def rotate(self):
        if self.direc_key == '>':
            self.direc_key = 'v'
        elif self.direc_key == 'v':
            self.direc_key = '<'
        elif self.direc_key == '<':
            self.direc_key = '^'
        elif self.direc_key == '^':
            self.direc_key = '>'

        self.guard_map[self.loc[0], self.loc[1]] = self.direc_key
        self.direc = np.array(self.guard_dirs[self.direc_key])

    def count_visits(self):
        x_counts = np.where(self.guard_map == 'X')
        return len(x_counts[0])

    def walk(self):
        # self.print_map()
        while True:
            # self.print_map()
            next_idx, next_field, stop_run = self.check_next()
            if stop_run:
                self.guard_map[self.loc[0], self.loc[1]] = 'X'
                return self.count_visits()
            if np.max(self.visited_locations) > 4:
                return -1
            if next_field != '.' and next_field != 'X':
                self.rotate()
            else:
                self.step_forward(next_idx)


class Day6:
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

        guard = Guard(data)
        guard.walk()
        answer = guard.count_visits()
        del guard

        print(f'Answer part 1 is : {answer}')

    def part2(self):
        data = self.load_text(self.file_name)

        guard = Guard(data)
        answer = guard.walk()
        data_walked = guard.guard_map
        del guard

        obsticals = np.where(data_walked == 'X')

        count_loops = 0
        for i in range(len(obsticals[0])):
            print(f'progress :{
                  i+1}/{len(obsticals[0])} {(i+1)/len(obsticals[0])*100}% ')
            obs = [obsticals[0][i], obsticals[1][i]]
            # no clue why data keeps changing
            data = self.load_text(self.file_name)

            guard = Guard(data)
            guard.guard_map[obs[0], obs[1]] = 'O'
            answer = guard.walk()
            del guard

            if answer < 0:
                count_loops = count_loops + 1

        print(f'Answer part 2 is : {count_loops}')


if __name__ == "__main__":
    # file_name = 'input/input_day6.txt'
    file_name = 'input/input_day6_test.txt'

    app = Day6(file_name)
    app.part1()
    app.part2()
