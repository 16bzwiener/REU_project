#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 13:27:10 2018

@author: benz
"""

import HexagonalLattice as HL
import numpy as np
import time

class BranchingFW:
    
    def __init__(self, steps=100, outputsize=(500,500), dim=2):
        
        # these are the fields
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim))
        self.__pos_list = [[self.__pos, 1, self.__pos]]
        self.__pos_list_dict = dict()
        self.__pos_list_dict[(self.__pos)] = 0
        self.__current_tips = [self.__pos]
        self.__root_node_color = "green"
        self.__root_edge_color = (0,.5,0,.5)
        self.__lattice.set_node_color(pos=self.__pos, color=self.__root_node_color)
        self.__deg = 45
            
    def step(self, pos):
        
        _, valid = self.__lattice.get_neighbors(pos)        

        count = 0
        while count < 25:
            rand = np.random.randint(len(valid))
            self.__pos = valid[rand]
            if self.__lattice.get_color_of_node(pos=self.__pos) == "orange":
                if hash(self.__pos) == hash(pos):
                    return False
                self.__pos_list.append([self.__pos, 1, pos])
                self.__pos_list_dict[self.__pos] = len(self.__pos_list) - 1
                self.__lattice.set_node_color(pos=self.__pos, color=self.__root_node_color)
                self.__lattice.expand_lattice(self.__pos)
                return True
            count+=1
            
        return False
            
    
    def branch(self):
        rand = np.random.randint(100)
        if rand > 45 and rand < 55:
            return True
        else: 
            return False
    
    def expand(self, pos):
        indices, neighb = self.__lattice.get_neighbors(pos)
        directions = []
        roots = []
        
        for n in neighb[:]:
            if self.__lattice.get_color_of_node(n) == self.__root_node_color:
                print('removed')
                neighb.remove(n)
                roots.append(n)
        
        for i, n in enumerate(neighb):
            direc = self.__lattice.get_direction_vector(pos, n)   
            directions.append(direc)
        
        rad = np.pi/(180/self.__deg)
        
        rotate_clockwise_matrix = ([[np.cos(rad), -np.sin(rad)],[np.sin(rad), np.cos(rad)]])
        rotate_counterclockwise_matrix = ([[np.cos(rad), np.sin(rad)],[np.sin(rad), np.cos(rad)]])
        print(rotate_clockwise_matrix)
        print(rotate_counterclockwise_matrix)
            
        """
        pairs = []
        
        for i in range(len(directions)):
            pairs.append(-1)
        
        for i, d1 in enumerate(directions):
            if pairs[i] == -1:
                for j, d2 in enumerate(directions):
                    if np.array_equal(d1, -d2):
                        pairs[i] = j
                        pairs[j] = i
        
        if len(pairs) > 0:                
            randIndex = np.random.randint(len(pairs))
            pairIndex = pairs[randIndex]
            self.__lattice.take_over_node(pos, neighb[randIndex])
            self.__pos_list[self.__pos_list_dict[pos]][1] += 1
            print(pairs)
            if pairIndex != -1:
                #print("NOT NEGATIVE ONE")
                self.__lattice.take_over_node(pos, neighb[pairIndex])
                self.__pos_list[self.__pos_list_dict[pos]][1] += 1
            #else:
                #print("WAS NEGATIVE ONE")
        """
        
    def walk(self, steps=10, j=2):
        for i in range(steps):
            for p in self.__current_tips[:]:
                #self.__lattice.display()
                self.__pos = p
                self.__current_tips.remove(p)
                if not self.step(p):
                    continue
                self.__current_tips.append(self.__pos)
                self.expand(self.__pos_list[-1][-1])
                rand = self.branch()
                if rand and self.__pos_list[-1][0] != self.__pos_list[-1][-1]:
                    self.__current_tips.append(p)
                    index = self.__pos_list_dict[self.__pos]
                    node = self.__pos_list[index]
                    while True:
                        k = self.__pos_list_dict[node[-1]]
                        node = self.__pos_list[k]
                        print(node)
                        self.expand(node[0])
                        if node[0] == (0,0):
                            break
                              
            if len(self.__current_tips) == 0:
                print(i)
                break 
        
        for i in range(len(self.__pos_list)-1):
            self.__lattice.set_edge_color(self.__pos_list[i+1][0], self.__pos_list[i+1][2], self.__root_edge_color)
        self.__lattice.display(save=1,outputsize=(2000,2000), filename="potential")
                   
    
walk = BranchingFW()
walk.walk()