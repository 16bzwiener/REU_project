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
      
    def get_random_state(self):
        return self.__lattice.get_graph_property_from_dictionary("state")
        
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
        if (rand > 45 and rand < 55) or rand > 80:
            return True
        else: 
            return False
    
    def expand(self, pos):
        indices, neighb = self.__lattice.get_neighbors(pos)
        directions = []
        directions_in_rad = []
        
        for n in neighb[:]:
            if self.__lattice.get_color_of_node(n) == self.__root_node_color:
                neighb.remove(n)
                rad = 0
                
                x = n[0]
                y = n[1]
                
                range_in_radians = (self.__deg/180)
                
                if x == 0:
                    rad = .5
                else:
                    rad = np.arctan(y/x)/np.pi
                
                if x < 0 or (x < 0 and y < 0):
                    rad+=1
                elif y < 0:
                    rad+=2
                
                lower = (rad - range_in_radians + 2) % 2
                upper = (rad + range_in_radians) % 2
                
                directions_in_rad.append([lower, upper])             
        
        for i, n in enumerate(neighb[:]):
            direc = self.__lattice.get_direction_vector(pos, n)
            direc_in_rad = 0
            
            x = direc[0]
            y = direc[1]
            
            if x != 0:
                direc_in_rad = np.arctan(y/x)/np.pi
            else:
                direc_in_rad = .5
            
            if x < 0 or (x < 0 and y < 0):
                direc_in_rad+=1
            elif y < 0:
                direc_in_rad+=2
                
            
            
            flag = False
        
            for r in directions_in_rad: 
                lower = r[0]
                upper = r[1]
                if lower < upper:
                    if direc_in_rad > upper or direc_in_rad < lower:
                        flag = True
                else:
                    if direc_in_rad < lower and direc_in_rad > upper:
                        flag = True
            
            if flag:
                directions.append(direc)
            else:
                neighb.remove(n)
        
        for n in neighb:
            self.__lattice.take_over_node(pos, n)
            self.__pos_list[self.__pos_list_dict[pos]][1] += 1
        
    def walk(self, steps=20, j=2):
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
                        self.expand(node[0])
                        if node[0] == (0,0):
                            break
                              
            if len(self.__current_tips) == 0:
                print(i)
                break
            print("HERE I AMMMMMMMMM ", i)
        filename = "potential" + str(time.time())
        for i in range(len(self.__pos_list)-1):
            self.__lattice.set_edge_color(self.__pos_list[i+1][0], self.__pos_list[i+1][2], self.__root_edge_color)
        self.__lattice.set_node_color((0,0), color="purple")
        self.__lattice.display(save=1,outputsize=(1000,1000), filename=filename)
        
        #self.__lattice.save("my_graph.xml.gz")
                   
state = np.random.get_state()   
walk = BranchingFW()
walk.walk()
np.random.set_state(walk.get_random_state())
walk2 = BranchingFW()
walk2.walk()