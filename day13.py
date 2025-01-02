# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import time
import re
import scipy

class Claw:
    def __init__(self, input_data):
        self.data = input_data
        self.dict_claws = {}
        self.get_claws(self.data)
        
    def get_claws(self,data):
        for i,ele in enumerate(data):
            # print('ele : ', ele)
            m =  self.get_num(ele)
            if not  i %3:
                X_A = m[0]
                Y_A = m[1]
                A = m            
            elif not (i-1) % 3:
                X_B = m[0]
                Y_B = m[1]
                B = m
            elif not (i-2)%3:
                X_P = m[0]
                Y_P = m[1]
                C = m
                self.dict_claws[int(i/3)] = [A,B,C]

    def get_ans_rec(self):
        self.tot_price = 0
        for key, value in self.dict_claws.items():
            print(value)
            self.visited = {}
            price = self.loop(0,0,value,0,0,0)
            
        return self.tot_price
    
    def dist(self,x,x_end,y,y_end):
        return np.sqrt((x_end-x)**2+(y_end-y)**2)

    def loop(self,x,y,claw,price,n_A,n_B):
        A = claw[0]
        B = claw[1]
        P = claw[2]
        print(n_A,n_B)

        if x == P[0] and y == P[1]:
            self.tot_price += price
            # print(price)
            return price
        
        if n_A >= 100 or n_B >= 100:
            return 0
        
        self.visited[(x,y)] = [self.dist(x,P[0],y,P[1]),n_A,n_B]
        self.visited =  dict(sorted(self.visited.items(), key=lambda item: item[0]))

        for key, value in self.visited.items():
            # dist_A = self.dist(x+A[0],P[0],y+A[1],P[1])
            # dist_B = self.dist(x+B[0],P[0],y+B[1],P[1])
                   

                if not (x+A[0],y+A[1]) in self.visited:
                    self.loop(x+A[0],y+A[1],claw,price + 3,n_A+1,n_B)
    
                if not (x+B[0],y+B[1]) in self.visited:
                    self.loop(x+B[0],y+B[1],claw,price + 1,n_A,n_B+1)
            # for i in range(2):
        

                # if i == 0 and not (x+A[0],y+A[1]) in self.visited:
                #     self.loop(x+A[0],y+A[1],claw,price + 3,n_A+1,n_B)
    
                # if i == 1 and not (x+B[0],y+B[1]) in self.visited:
                #     self.loop(x+B[0],y+B[1],claw,price + 1,n_A,n_B+1)
                        
    	        
    def get_ans(self,claw,add_P):
        A = claw[0]
        B = claw[1]
        P = claw[2]
        P[0] += add_P
        P[1] += add_P
        a = A[0]
        b = B[0]
        c = A[1]
        d = B[1]
        AB = np.array([[a,b],[c,d]])
        x = P[0]
        y = P[1]
    
        pre = 1/(a*d-b*c)
        ans = [pre*(d*x-b*y),pre*(-c*x+a*y)]
        # ans = np.linalg.solve(AB,P)
        print(ans)
        threshold = 1e-3
        is_int = (abs(ans[0]-round(ans[0])) <  threshold) and (abs(ans[1]-round(ans[1])) < threshold)
        return ans, is_int

    def solve_all(self,add_P):
        price = int(0)
        for key, value in self.dict_claws.items():
            ans, is_int = self.get_ans(value,add_P)
            if is_int:
                price += ans[0]*3+ans[1]
        return price

    def get_num(self,str_in):
        patern = r'\d+'
        m = re.findall(r'\d+',str_in)
        m_new = [int(item) for item in m]
        return m_new



class Day12:
    def __init__(self, file_name_input):
        self.file_name = file_name_input

    def load_text(self, file_name_load):
        file = open(file_name_load, "r")
        data_raw = file.read()
        data_raw = data_raw.split('\n')
        file.close()
        data_output = []
        for line in data_raw:
            if len(line) > 0:
                data_output.append((line))
        return data_output

    def part1(self):
        data = self.load_text(self.file_name)
        # print(data)
        claw = Claw(data)
        
        price = claw.solve_all(0)
        
        self.x = claw
        # print(self.x.dict_claws)
        ans = price
        print(f'Answer part 1 is : {ans}')
        

    def part2(self):
        data = self.load_text(self.file_name)
        # print(data)
        claw = Claw(data)
        
        price = claw.solve_all(10000000000000)
        
        self.x = claw
        # print(self.x.dict_claws)
        ans = price
        print(f'Answer part 2 is : {ans}')
        
    def part1_rec(self):
        data = self.load_text(self.file_name)
        # print(data)
        claw = Claw(data)
        
        price = claw.get_ans_rec()
        
        self.x = claw
        # print(self.x.dict_claws)
        ans = price
        print(f'Answer part 1 is : {ans}')

if __name__ == "__main__":
    file_name = 'input/input_day13.txt'
    # file_name = 'input/input_day13_test.txt'
    # file_name = 'input/input_day13_test2.txt'
    # file_name = 'input/input_day13_test3.1txt'
    # file_name = 'input/input_day13_test4.txt'

    app = Day12(file_name)
    start = time.time()
    app.part1()
    end = time.time()
    print(f'evaluation time part 1 :  {end - start} sec')
    
    # app = Day12(file_name)
    # start = time.time()
    # app.part1_rec()
    # end = time.time()
    # print(f'evaluation time part 1 rec : {end - start} sec')
    
    start = time.time()
    app.part2()
    end = time.time()
    print(f'evaluation time part 2 : {end - start} sec')