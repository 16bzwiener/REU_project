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
        
        # these are the fields
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim))
        self.__pos_list = [[self.__pos, 1, self.__pos]]
        self.__current_tips = [self.__pos]
        self.__root_color = "green"
        self.__lattice.set_node_color(pos=pos, color=self.__root_color)
        #self.walk()
            
    def step(self, pos):
        
        _, valid = self.__lattice.get_neighbors(pos)#LD.surrounding(pos, setting=0) #[LD.right(pos)], 1
        
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
        
        indices, neighb = lattice.get_neighbors(self.__pos)
        
        directions = []
        
        for i, n in enumerate(neighb):
            direc = self.__lattice.get_direction_vector(self.__pos, n)   
            directions.append(direc)
        
        pairs = []
        for i in range(len(directions)):
            pairs.append(-1)
            
        print(pairs)
            
        '''
        for (i, p) in enumerate(self.__pos_list):
            if i > 0 and self.__pos_list[i-1][1] <= self.__pos_list[i][1]:
                continue
            pos1 = p[0]
            n, _ = self.__lattice.get_neighbors(pos1)
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
        '''
            
    def walk(self, steps=50, j=2):
        self.expand()
        '''
        # this branches
        for i in range(steps):
            
            # call the expansion function every j steps
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
         '''   
#    def walk2(self, steps=50):
#        for i in range(steps):
            
    
walk = BranchingFW()
walk.walk()