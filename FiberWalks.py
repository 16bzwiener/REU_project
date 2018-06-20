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

class BranchingFW:
    
    def __init__(self, steps=100, outputsize=(500,500), dim=2):
        
        # these are the fields
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim))
        self.__pos_list = [[self.__pos, 1, self.__pos]]
        self.__current_tips = [self.__pos]
        self.__root_node_color = "green"
        self.__root_edge_color = (0,.5,0,.5)
        self.__lattice.set_node_color(pos=self.__pos, color=self.__root_node_color)
        #self.walk()
            
    def step(self, pos):
        
        _, valid = self.__lattice.get_neighbors(pos)#LD.surrounding(pos, setting=0) #[LD.right(pos)], 1
        
        for i in valid[:]:
            if self.__lattice.get_color_of_node(pos=i) != "orange":
                valid.remove(i)
        
        if len(valid) > 0:
            rand = np.random.randint(len(valid))
            self.__pos = valid[rand]
            if hash(self.__pos) == hash(pos):
                return False
            self.__pos_list.append([self.__pos, 1, self.__pos_list[-1][0]])
            self.__lattice.set_node_color(pos=self.__pos, color=self.__root_node_color)
            self.__lattice.set_edge_color(self.__pos,pos,self.__root_edge_color)
            self.__lattice.expand_lattice(self.__pos)
            self.__lattice.display()
            return True
            
    
    def branch(self):
        rand = np.random.randint(100)
        if rand > 45 and rand < 55:
            return True
        else: 
            return False
    
    def expand(self, pos):
        indices, neighb = self.__lattice.get_neighbors(pos)
        directions = []
        
        for n in neighb[:]:
            if self.__lattice.get_color_of_node(n) == self.__root_node_color:
                print('removed')
                neighb.remove(n)
        
        for i, n in enumerate(neighb):
            direc = self.__lattice.get_direction_vector(pos, n)   
            directions.append(direc)
        
        
        print(directions)
        print(pos)
        
        pairs = []
        
        for i in range(len(directions)):
            pairs.append(-1)
        
        for i, d1 in enumerate(directions):
            if pairs[i] == -1:
                for j, d2 in enumerate(directions):
                    if np.array_equal(d1, -d2):
                        pairs[i] = j
                        pairs[j] = i
                        
        randIndex = np.random.randint(len(pairs))
        pairIndex = pairs[randIndex]
        self.__lattice.take_over_node(pos, neighb[randIndex])
        print(pairs)
        if pairIndex != -1:
            print("NOT NEGATIVE ONE")
            self.__lattice.take_over_node(pos, neighb[pairIndex])
        else:
            print("WAS NEGATIVE ONE")
            
    def walk(self, steps=2, j=2):
        for i in range(steps):
            for p in self.__current_tips[:]:
                print(list(self.__lattice.get_edge_colors()))
                self.__lattice.display()
                self.__pos = p
                self.__current_tips.remove(p)
                if not self.step(p):
                    continue
                self.__current_tips.append(self.__pos)
                self.expand(self.__pos_list[-1][-1])
                rand = self.branch()
                if rand and self.__pos_list[i] != self.__pos_list[i+1]:
                    self.__current_tips.append(p)
                    
                
            if len(self.__current_tips) == 0:
                break 
        
        print(list(self.__lattice.get_edge_colors()))
        self.__lattice.display()
        
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