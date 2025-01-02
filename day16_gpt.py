import numpy as np
import time
import heapq

class Reindeer:
    def __init__(self, input_data):
        self.load_map(input_data)
        self.find_start_end()
        self.map_visit = self.map.copy()
        self.start_dir = (0, 1)
        self.count_loc()

        self.dir_all = ((0, 1), (0, -1), (1, 0), (-1, 0))

        self.set_open = []
        self.set_closed = set()

    def load_map(self, data_input):
        self.map = data_input

    def count_loc(self):
        self.total_locs = len(np.where(self.map == '.')[0])

    def find_start_end(self):
        loc_start = np.where(self.map == 'S')
        loc_end = np.where(self.map == 'E')

        self.loc_start = (loc_start[0][0], loc_start[1][0])
        self.loc_end = (loc_end[0][0], loc_end[1][0])
        return (self.loc_start, self.loc_end)

    def add_to_open(self, node):
        heapq.heappush(self.set_open, node)

    def dist_end(self,loc):
        return np.sqrt((loc[0]-self.loc_end[0])**2 + (loc[1]-self.loc_end[1])**2)

    def get_lowest_f(self, fin_score):
        while self.set_open:
            node = heapq.heappop(self.set_open)
            score = node[0]  # Assuming score is the first element in the tuple
            if score >= fin_score:
                self.set_closed.add(node)
                continue
            return node
        return None

    def check_for_equal(self, node, check_list):
        for check_node in check_list:
            if check_node[1] == node[1] and (check_node[2] == node[2] or check_node[2] == (-node[2][0], -node[2][1])):
                return True, check_node
        return False, node

    def add_neigbors(self, neighbor_nodes):
        for node in neighbor_nodes:
            check, nodes_repeated = self.check_for_equal(node, self.set_open)
            if check:
                if nodes_repeated[0] > node[0]:
                    self.set_open.remove(nodes_repeated)
                    self.add_to_open(node)
            else:
                self.add_to_open(node)

    def get_next(self, node):
        loc = node[1]
        direc = node[2]
        h_score = node[0]
        neighbor_nodes = set()
        for direction in self.dir_all:
            loc_check = (loc[0] + direction[0], loc[1] + direction[1])
            if (0 <= loc_check[0] < self.map.shape[0] and 0 <= loc_check[1] < self.map.shape[1]):
                loc_sign = self.map[loc_check]
                if loc_sign == '.' or loc_sign == 'E':
                    if direc == direction:
                        neighbor_nodes.add((h_score + 1, loc_check, direction, self.loc_end))
                    elif direc == (-direction[0], -direction[1]):
                        continue
                    else:
                        neighbor_nodes.add((h_score + 1001, loc_check, direction, self.loc_end))
        return neighbor_nodes

    def solve(self):
        loc_start, loc_end = self.find_start_end()
        start_node = (0, loc_start, self.start_dir, loc_end)
        self.add_to_open(start_node)

        i = 0
        end_loop = 1000000
        while self.set_open and i < end_loop:
            i += 1
            print(f'\riterations : {i}, length open : {len(self.set_open)}, length closed : {len(self.set_closed)}', end="")

            current = self.get_lowest_f(float('inf'))
            if current is None:
                break

            self.set_closed.add(current)
            self.map_visit[current[1]] = '0'

            neighbor_nodes = self.get_next(current)
            self.add_neigbors(neighbor_nodes)

            if self.map[current[1]] == 'E':
                print(f"End reached with score: {current[0]}")
                return current[0]
        return -1


class Day16:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        with open(file_name_load, "r") as file:
            data_raw = file.read().split('\n')
        return np.array([list(line) for line in data_raw if line])

    def part1(self):
        map_input = self.load_text(self.file_name)
        reindeer = Reindeer(map_input)
        result = reindeer.solve()
        print(f'Answer part 1 is: {result}')

    def part2(self):
        # Implement part2
        pass


if __name__ == "__main__":
    # plt.close('all')

    file_name = 'input/input_day16.txt'
    # file_name = 'input/input_day16_test.txt'
    # file_name = 'input/input_day16_test2.txt'
    # file_name = 'input/input_day16_test3.txt'
    # file_name = 'input/input_day16_test4.txt'
    app = Day16(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'\nEvaluation time part 1: {end - start} sec')

    start = time.time()
    app.part2()
    end = time.time()
    print(f'Evaluation time part 2: {end - start} sec')
