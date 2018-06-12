#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 13:27:10 2018

@author: benz
"""

import LatticeDirections as LD
import HexagonalLattice as HL
import numpy as np
import time

root_color = "green"        
lattice = HL.HexagonalLattice(vertex_color="orange", outputsize=(500,500))
lattice.set_node_color(pos=(0,0), color=root_color)
pos = (0,0)
valid = []

class BranchingFW:
    
    def __init__(self, steps=100, outputsize=(500,500), dim=2):
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim))
        self.__pos_list = [[self.__pos, 1, self.__pos]]
        self.__current_tips = [self.__pos]
        self.__root_color = "green"
        self.__lattice.set_node_color(pos=pos, color=self.__root_color)
        self.walk()
            
    def step(self, pos):
        
        valid = self.__lattice.get_neighbors(pos, sys=1)#LD.surrounding(pos, setting=0) #[LD.right(pos)], 1
        
        for i in valid[:]:
            if self.__lattice.get_color_of_node(pos=i) != "orange":
                valid.remove(i)
        
        if len(valid) > 0:
            rand = np.random.randint(len(valid))
            pos = valid[rand]
            #d = np.subtract()
            while self.__lattice.is_lost_node(pos):
                valid = [LD.right(valid[0])]
            self.__lattice.set_node_color(pos=pos, color=self.__root_color)
            self.__lattice.expand_lattice(pos)
            
        #find_off_limits(pos)
            
        return tuple(pos) 
    
    def branch(self):
        rand = np.random.randint(100)
        if rand > 45 and rand < 55:
            return True
        else: 
            return False
    
    def expand(self):
        for (i, p) in enumerate(self.__pos_list):
            if i > 0 and self.__pos_list[i-1][1] <= self.__pos_list[i][1]:
                continue
            pos1 = p[0]
            n = self.__lattice.get_neighbors(pos1)
            flag = False
            for index in n:
                pos2 = self.__lattice.get_from_dictionary(int(index))
                if self.__lattice.get_color_of_node(pos2) == "orange":
                    flag = True
                    self.__lattice.take_over_node(pos1, pos2)
            if flag:
                self.__pos_list[i][1]+=1
            
            print(np.subtract(p[0],p[2]))
        return 1
            
    def walk(self, steps=50):
        # this branches
        for i in range(steps):
            if (i + 1) % 2 == 0:
                self.expand()
            for p in self.__current_tips[:]:
                self.__current_tips.remove(p)
                pos= self.step(p)
                if p != pos:
                    self.__lattice.set_edge_color(p,pos,(0,.5,0,.5))
                    self.__pos_list.append([pos, 1, p])
                    self.__current_tips.append(pos)
                    rand = self.branch()
                    if rand and self.__pos_list[i] != self.__pos_list[i+1]:
                        self.__current_tips.append(p)
            if len(self.__current_tips) == 0:
                break
            print(i)
        self.__lattice.display(save=1, outputsize=(2000,2000))
        for i in self.__pos_list:
            print(i[1])
    
walk = BranchingFW()

'''
def direction(self, pos1, pos2):
        pos1 = tuple(pos1)
        pos2 = tuple(pos2)
        pos3 = tuple(np.absolute(np.subtract(pos1, pos2)))
        if pos3 == (2,0):
            # it is right!
            if tuple(np.add(pos1, (2,0))) == pos2:
                return LD.right_shared(pos1)
            # it is left
            else:
                return LD.left_shared(pos1)
        else:
            if tuple(np.add(pos1, (1,2))) == pos2:
                return LD.lower_right_shared(pos1)
            elif tuple(np.add(pos1, (1,-2))) == pos2:
                return LD.upper_right_shared(pos1)
            elif tuple(np.add(pos1, (-1,2))) == pos2:
                return LD.lower_left_shared(pos1)
            else:
                return LD.upper_left_shared(pos1)

def find_off_limits(pos):
    
    color = lattice.get_color_of_node(pos)

    surround = [LD.right(pos), LD.upper_right(pos), LD.upper_left(pos), LD.left(pos), 
             LD.lower_left(pos), LD.lower_right(pos)]

    p = LD.right(LD.right(pos))
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")        
    
    p = LD.upper_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")

    p = LD.upper_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")
    
    p = LD.left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")

    p = LD.left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")
    
    p = LD.lower_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
    
    p = LD.lower_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
    
    p = LD.lower_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")

    p = LD.lower_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")
    
    p = LD.right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")

    p = LD.right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")
    
    p = LD.upper_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")

def step(pos, valid_prev):
        
    valid, _ = LD.surrounding(pos, setting=1)
    for i in valid[:]:
        if lattice.get_color_of_node(pos=i) != "orange" or i in valid_prev:
            valid.remove(i)
    
    if len(valid) > 0:
        rand = np.random.randint(len(valid))
        pos = valid[rand]
        lattice.set_node_color(pos=pos, color=root_color)
        lattice.expand_lattice(pos)
        
    #find_off_limits(pos)
        
    return tuple(pos), valid    

def contraction(pos):
    
    for p in list:
        lattice.take_over_node(pos, p)
        
posList = [pos]
currentTips = [pos]

# this branches
for i in range(50):
    for p in currentTips[:]:
        currentTips.remove(p)
        rand = np.random.randint(100)
        pos, valid = step(p, valid)
        if p != pos:
            lattice.set_edge_color(p,pos,(0,.5,0,.5))
        posList.append(pos)
        currentTips.append(pos)
        if rand > 45 and rand < 55 and posList[i] != posList[i+1]:
            currentTips.append(p)
        #time.sleep(2)
        #lattice.display()
    if len(currentTips) == 0:
        break
    print(i)

lattice.display()
'''