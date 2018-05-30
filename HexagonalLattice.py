#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:20:30 2018

@author: Benjamin Zwiener
"""

import numpy as np
import graph_tool.all as gt

# the directions are only implemented for 2-D     
def right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([2,0]))

def left(point: np.ndarray) -> np.ndarray:
    return (point + np.array([-2,0]))

def upper_right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([1,-2]))

def lower_right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([1,2]))

def upper_left(point: np.ndarray) -> np.ndarray:
    return (left(upper_right(point)))

def lower_left(point: np.ndarray) -> np.ndarray:
    return (left(lower_right(point)))

class HexagonalLattice:
    
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
        self.add_vertex(pos)
    
    def increase_size(self, size=1):
        self.__size+=size
    
    # add to the dictionary that maps coordinates to vertex number
    def add_to_dict(self, point, vertex_index):
        self.__dictionary[tuple(point)] = vertex_index
        self.increase_size()
        
    def add_vertex(self, pos):
        if not self.check_for_node(pos):
            v = self.__GD.add_vertex()
            self.add_to_dict(tuple(pos), v)
            self.__pos[v] = pos
        
    def display(self):
        gt.graph_draw(self.__GD, pos=self.__pos, vertex_font_size=12,
            output_size=self.__outputsize)
        
    def get_dictionary(self):
        return self.__dictionary
    
    def get_size(self):
        return self.__size
    
    def connect(self, pos1, pos2):
                    
        if tuple(pos2) in self.__dictionary:
            return False
        else:
            self.add_vertex(pos2)
            self.__GD.add_edge(self.get_vertex(pos1), self.get_vertex(pos2))
            return True
            
    def get_vertex(self, pos):
        return self.__GD.vertex(self.__dictionary[tuple(pos)])
    
    def check_for_node(self, pos):
        if tuple(pos) in self.__dictionary:
            return True
        else:
            return False
