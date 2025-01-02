# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:18:46 2024

@author: RobinMak
"""
import numpy as np
import itertools


class Diskmap:
    def __init__(self, input_data):
        self.data = input_data
        self.diskmap = np.array([])
        pass
    
    def get_step1(self,data):
        diskmap_temp = np.array([])
        for i,ele_str in enumerate(data):
            ele = int(ele_str)
            if i % 2: #odd
                diskmap_temp=np.append(diskmap_temp,['.' for x in range(ele)])
            else: # even
                diskmap_temp=np.append(diskmap_temp,[str(int(i/2)) for x in range(ele)])
        return diskmap_temp
        
    def get_step2(self,diskmap_temp):
        loc_space = np.where(diskmap_temp == '.')
        loc_nospace = np.where(diskmap_temp != '.')
        
        print(loc_space[0],loc_nospace[0])
        print(len(loc_space[0]),len(loc_nospace[0]))
        print(diskmap_temp)

        for i,ele in enumerate(loc_space[0]):
            ix1 = loc_space[0][i]
            ix2 = loc_nospace[0][-i-1]
            
            if ix1 > ix2:
                break
            diskmap_temp[[ix1, ix2]] = diskmap_temp[[ix2, ix1]]
            print(diskmap_temp)
        return diskmap_temp
        
    def checksum(self,diskmap):
        tot_sum = 0
        for i,ele in enumerate(diskmap):
            if ele != '.':
                tot_sum += i*int(ele)
        return tot_sum
    
    def group_string(self,diskmap):
        new_diskmap = np.array([])
        last_el = ''
        temp_string = ''
        for i,ele in enumerate(diskmap):
            # print(ele)
            # print(temp_string)
            if ele == last_el:
                temp_string += ele
            else:
                if temp_string != '':
                    new_diskmap = np.append(new_diskmap,temp_string)
                temp_string = ele
                last_el = ele
        new_diskmap = np.append(new_diskmap,temp_string)

        return new_diskmap
     
    def rearange_old(self, diskmap):
        diskmap_temp = diskmap
        # idx = np.find(diskmap,'.')
        # print(diskmap)
        # idx = np.flatnonzero(diskmap == '.')
        diskmap_idx = np.arange(0,len(diskmap),1)
        diskmap_space = diskmap[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        diskmap_space_idx = diskmap_idx[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        
        diskmap_nospace = diskmap[np.char.find(diskmap, sub = '.', start = 0, end = None)<0]
        diskmap_nospace_idx = diskmap_idx[np.char.find(diskmap, sub = '.', start = 0, end = None)<0]
        
        
        
        # print(diskmap_nospace,diskmap_nospace_idx)
        # print(diskmap_space,diskmap_space_idx)
        # print(diskmap_space)
        
        for X,i_space in enumerate(diskmap_space_idx):
            for X,i_nospace in enumerate(diskmap_nospace_idx[::-1]):
                print(diskmap[i_space],diskmap[i_nospace])
                # print(len(ele_space),len(ele_nospace))
                if len(diskmap[i_space]) >= len(diskmap[i_nospace]):
                    print('through')
                    ix1 = i_space
                    ix2 = i_nospace
                    print(ix1, ix2,i_nospace)

                    # if ix1 < ix2:
                    #     break
                    # diskmap_nospace
                    diskmap_temp[[ix1, ix2]] = diskmap_temp[[ix2, ix1]]
                    # diskmap_nospace = np.delete(diskmap_nospace,i_nospace)
                    print(diskmap_temp)        

                    break

    def rearange(self, diskmap):
        # idx = np.find(diskmap,'.')
        print(diskmap)
        # idx = np.flatnonzero(diskmap == '.')

        diskmap_idx = np.arange(0,len(diskmap),1)
        diskmap_nospace = diskmap[np.char.find(diskmap, sub = '.', start = 0, end = None)<0]
        diskmap_nospace_idx = diskmap_idx[np.char.find(diskmap, sub = '.', start = 0, end = None)<0]
        diskmap_space = diskmap[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        diskmap_space_idx = diskmap_idx[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        
        return self.reareange_loop(diskmap,diskmap_nospace,diskmap_nospace_idx)
        
    
    def reareange_loop(self,diskmap,diskamp_nospace,diskmap_nospace_idx):
        diskmap_temp = diskmap

        diskmap_idx = np.arange(0,len(diskmap),1)
        diskmap_space = diskmap[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        diskmap_space_idx = diskmap_idx[np.char.find(diskmap, sub = '.', start = 0, end = None)>=0]
        for X,i_space in enumerate(diskmap_space_idx):
            for idx_ele,i_nospace in enumerate(diskmap_nospace_idx[::-1]):
                print(diskmap[i_space],diskmap[i_nospace])
                # print(len(ele_space),len(ele_nospace))
                diff_len1 = len(diskmap[i_space]) - len(diskmap[i_nospace])
                diff_len2 = len(diskmap[i_nospace]) - len(diskmap[i_space])
                print(diff_len1)
                if diff_len1 >= 0 :
                    print('through')
                    ele = diskmap[i_nospace]
                    ix1 = i_space
                    ix2 = i_nospace
                    print(ix1, ix2,i_nospace)
                    diskmap_temp[i_space] = '.'*diff_len1 
                    if len(diskmap[i_space]) > 0:
                        diskmap_temp[i_nospace] = '.'*diff_len2  
                    
                    diskmap_temp = np.delete(diskmap_temp, i_nospace)
                    diskmap_temp = np.insert(diskmap_temp, i_space, ele)
                    
                    print(diskmap_temp)        
                    
                    # diskamp_nospace = np.delete(diskamp_nospace,idx_ele)
                    # diskmap_nospace_idx = np.delete(diskmap_nospace_idx,idx_ele)
                                        
                    self.reareange_loop(diskmap_temp,diskamp_nospace,diskmap_nospace_idx)

                    break
        return diskmap_temp
                
    
    def get_diskmap_part1(self):
        diskmap_temp = self.get_step1(self.data)
        diskmap = self.get_step2(diskmap_temp)
        tot_sum = self.checksum(diskmap)
        return diskmap,tot_sum

    def get_diskmap_part2(self):
        diskmap_temp = self.get_step1(self.data)
        diskmap_temp = self.group_string(diskmap_temp)
        self.diskmap_last = []
        diskmap_temp = self.rearange(diskmap_temp)
        # self.diskmap_temp = diskmap_temp
        print(diskmap_temp)
        # diskmap = self.get_step3(diskmap_temp)
        # tot_sum = self.checksum(diskmap)
        # return diskmap,tot_sum


class Day9:
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
        data = self.load_text(self.file_name)[0]
        # data = np.array(['1','2','3','4','5'])
        # print(data)
        diskmap = Diskmap(data)
        diskmap_ans,sum_ans = diskmap.get_diskmap_part1()
        
        print('map: ', (diskmap_ans))

        answer = -1        

        print(f'Answer part 1 is : {sum_ans}')

    def part2(self):
        data = self.load_text(self.file_name)[0]
        diskmap = Diskmap(data)
        diskmap.get_diskmap_part2()
        # self.diskmap = diskmap
        # diskmap_ans,sum_ans = diskmap.get_diskmap_part2()
        answer = -1        
        print(f'Answer part 2 is : {answer}')


if __name__ == "__main__":
    # file_name = 'input/input_day9.txt'
    file_name = 'input/input_day9_test.txt'
    app = Day9(file_name)
    app.part1()
    # app.part2()
