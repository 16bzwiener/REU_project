#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:54:10 2018

@author: benz
"""

import numpy as np
import HexagonalLattice as HL
import time

class BasicFiberWalk():
    
    def __init__(self, steps=100, outputsize=(200,200)):
        self.__lattice = HL.HexagonalLattice2D(outputsize=outputsize)
        self.__pos = (0,0)
        self.__pos_list = [self.__pos]
        self.walk(steps)
        
        
    def walk(self, goalsteps):
        times = 0
        steps = 0
        while steps < goalsteps and times < 6:

            valid = self.__lattice.get_valid_neighbors(self.__pos)      
                        
            if len(valid) > 0:
                rand = np.random.randint(len(valid))
                
                self.__pos = valid[rand]
                self.__lattice.change_node_color(self.__pos)
                self.__lattice.expand_lattice(self.__pos)
                self.__pos_list.append(self.__pos)
                steps+=1
                
                self.display()
            else:
                print(steps)
                print("root was blocked")
                print(self.__pos_list)
                break
            
            time.sleep(.1)
            
        
    def display(self):
        self.__lattice.display()
        
#walk = BasicFiberWalk(steps = 500, outputsize=(500,500))
        
class ImprovedFiberWalk():
    
    def __init__(self, steps=100, outputsize=(200,200), dim=2):
        self.__lattice = HL.HexagonalLattice2D(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim, dtype=int))
        self.__pos_list = [self.__pos]
        self.__off_limits = set()
        
    def step(self):
        
        valid = self.__lattice.get_valid_neighbors(self.__pos)
        
        new_valid = []
        for v in valid[:]:
            if tuple(v) in self.__off_limits:
                valid.remove(tuple(v))
    
        if len(valid) > 0:
            rand = np.random.randint(len(valid))
            rand = valid[rand]

            for i in valid:
                self.__off_limits.add(tuple(i))
            self.__pos = rand
            self.__lattice.change_node_color(self.__pos)
            self.__lattice.expand_lattice(self.__pos)
            self.__pos_list.append(self.__pos)
            
            
            self.display()
            #time.sleep(2)
            return False
        else:
            print("root was blocked")
            print(self.__pos_list)
            return True
            
    def direction(self, pos1, pos2):
        pos3 = tuple(np.absolute(np.subtract(pos1, pos2)))
        if pos3 == (2,0):
            # it is right!
            if tuple(np.add(pos1, (2,0))) == pos2:
                return HL.right_shared(pos1)
            # it is left
            else:
                return HL.left_shared(pos1)
        else:
            if tuple(np.add(pos1, (1,2))) == pos2:
                return HL.lower_right_shared(pos1)
            elif tuple(np.add(pos1, (1,-2))) == pos2:
                return HL.upper_right_shared(pos1)
            elif tuple(np.add(pos1, (-1,2))) == pos2:
                return HL.lower_left_shared(pos1)
            else:
                return HL.upper_left_shared(pos1)
        
    def display(self):
        self.__lattice.display()
        
    def get_off_limits(self):
        return self.__off_limits
    
    def random_contraction(self):
        i = np.random.randint(len(self.__pos_list))
        j = np.random.randint(len(self.__pos_list))
        
        self.__lattice.take_over_node(self.__pos_list[i], self.__pos_list[j])
        
walk = ImprovedFiberWalk(outputsize=(500,500))
while True:
    if walk.step(): break
print(walk.get_off_limits())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
