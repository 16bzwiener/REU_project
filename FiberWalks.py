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
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = (0,0)
        self.walk(steps)
        
        
    def walk(self, goalsteps):
        times = 0
        steps = 0
        while steps < goalsteps and times < 6:

            valid = self.__lattice.get_valid_neighbors(self.__pos)      
            print(valid)
            
            if len(valid) > 0:
                rand = np.random.randint(len(valid))
                print(valid[rand])
                
                self.__pos = valid[rand]
                self.__lattice.change_node_color(self.__pos)
                self.__lattice.expand_lattice(self.__pos)
                
                steps+=1
                
                self.display()
            else:
                print(steps)
                print("root was blocked")
                break
            
            time.sleep(.1)
            
        
    def display(self):
        self.__lattice.display()
        
walk = BasicFiberWalk(steps = 500, outputsize=(500,500))