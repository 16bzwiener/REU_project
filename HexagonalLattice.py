#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:20:30 2018

@author: Benjamin Zwiener
"""

import numpy as np
import graph_tool.all as gt

class Hex_lattice:
    
    def __init__(self, dim=2, size=0, outputsize=(200,200)):
        self.__dimension = dim
        self.__size = size
        self.__outputsize = outputsize
        self.__GD = gt.Graph(directed=False)
        self.__pos = self.__GD.new_vertex_property("vector<double>")
        self.__dictionary = dict()
        pos = []
        for i in range(dim):
            pos.append(float(0.0))
        v1 = self.__GD.add_vertex()
        self.add_to_dict(tuple(pos), v1)
        self.expandLattice(pos)
    
    def increase_size(self, size=1):
        self.__size+=size
    
    # the directions are only implemented for 2-D     
    def right(self, point: np.ndarray) -> np.ndarray:
        return (point + np.array([2,0]))

    def left(self, point: np.ndarray) -> np.ndarray:
        return (point + np.array([-2,0]))
    
    def upper_right(self, point: np.ndarray) -> np.ndarray:
        return (point + np.array([1,-2]))
    
    def lower_right(self, point: np.ndarray) -> np.ndarray:
        return (point + np.array([1,2]))
    
    def upper_left(self, point: np.ndarray) -> np.ndarray:
        return (self.left(self.upper_right(point)))
    
    def lower_left(self, point: np.ndarray) -> np.ndarray:
        return (self.left(self.lower_right(point)))
    
    # add to the dictionary that maps coordinates to vertex number
    def add_to_dict(self, point, vertex_index):
        self.__dictionary[tuple(point)] = vertex_index
        self.increase_size()
    
    def expandLattice(self, pos):
        if tuple(pos) in self.__dictionary:
            self.add_vertex(self.right(pos))
            self.add_vertex(self.upper_right(pos))
            self.add_vertex(self.upper_left(pos))
            self.add_vertex(self.left(pos))
            self.add_vertex(self.lower_left(pos))
            self.add_vertex(self.lower_right(pos))
        
    def add_vertex(self, pos):
        if tuple(pos) not in self.__dictionary:
            v = self.__GD.add_vertex()
            self.add_to_dict(tuple(pos), v)
            self.__pos[v] = pos
        
    def display(self):
        gt.graph_draw(self.__GD, pos=self.__pos, vertex_font_size=18,
            output_size=self.__outputsize)
        
    def get_dictionary(self):
        return self.__dictionary
    
    def get_size(self):
        return self.__size
    
    def connect_random(self, pos):
        rn = np.random.randint(6)
        randpos = None
        
        if rn == 0:
            randpos = self.right(pos)
        if rn == 1:
            randpos = self.upper_right(pos)
        if rn == 2:
            randpos = self.upper_left(pos)
        if rn == 3:
            randpos = self.left(pos)
        if rn == 4:
            randpos = self.lower_left(pos)
        if rn == 5:
            randpos = self.lower_right(pos)
            
        if randpos is not None and tuple(randpos) in self.__dictionary:
            self.__GD.add_edge(self.get_vertex(pos), self.get_vertex(randpos))
        else:
            self.add_vertex(randpos)
            self.__GD.add_edge(self.get_vertex(pos), self.get_vertex(randpos))
            
    def get_vertex(self, pos):
        return self.__GD.vertex(self.__dictionary[tuple(pos)])
        
lattice = Hex_lattice(outputsize=(500,500))

for i in range(10):
    keys = lattice.get_dictionary().keys()
    rn = np.random.randint(lattice.get_size())
    rp = list(keys)[rn]
    lattice.expandLattice(rp)

for i in range(50):
    keys = lattice.get_dictionary().keys()
    rpList = list(keys)
    rn = np.random.randint(lattice.get_size())
    rp = rpList[rn]
    print(i)
    lattice.connect_random(rp)

lattice.display()
