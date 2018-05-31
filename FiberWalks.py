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
        self.__pos = (2,0)
        self.walk(steps)
        
    def walk(self, goalsteps):
        times = 0
        steps = 0
        while steps < goalsteps and times < 6:
            flag = False
            times = 0
            while not flag and times < 6:
                rn = np.random.randint(6)
                randpos = None
                pos = np.array(self.__pos)
                #valid_list = []
                if rn == 0:
                    randpos = HL.right(pos)
                if rn == 1:
                    randpos = HL.upper_right(pos)
                if rn == 2:
                    randpos = HL.upper_left(pos)
                if rn == 3:
                    randpos = HL.left(pos)
                if rn == 4:
                    randpos = HL.lower_left(pos)
                if rn == 5:
                    randpos = HL.lower_right(pos)
                    
                flag = self.__lattice.connect(self.__pos, randpos)
                
                times+=1
            
            self.__pos = tuple(randpos)
            
            steps+=1
            
        self.display()
            
            #time.sleep(2)
            
        print()
            
        
    def display(self):
        self.__lattice.display()
        
walk = BasicFiberWalk(steps = 500)