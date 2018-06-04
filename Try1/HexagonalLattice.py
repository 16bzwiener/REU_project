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
    return (point + np.array([1,-1*np.sqrt(3)]))

def lower_right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([1,np.sqrt(3)]))

def upper_left(point: np.ndarray) -> np.ndarray:
    return (left(upper_right(point)))

def lower_left(point: np.ndarray) -> np.ndarray:
    return (left(lower_right(point)))

def right_shared(point: np.ndarray) -> np.ndarray:
    return upper_right(point), lower_right(point)

def upper_right_shared(point: np.ndarray) -> np.ndarray:
    return right(point), upper_left(point)

def upper_left_shared(point: np.ndarray) -> np.ndarray:
    return upper_right(point), left(point)

def left_shared(point: np.ndarray) -> np.ndarray:
    return upper_left(point), lower_left(point)

def lower_left_shared(point: np.ndarray) -> np.ndarray:
    return left(point), lower_right(point)

def lower_right_shared(point: np.ndarray) -> np.ndarray:
    return right(point), lower_left(point)

class HexagonalLattice2D:
    
    def __init__(self, dim=2, size=0, outputsize=(200,200)):
        self.__dimension = dim
        self.__size = size
        self.__outputsize = outputsize
        self.__GD = gt.Graph(directed=False)
        self.__pos = self.__GD.new_vertex_property("vector<double>")
        self.__colors = self.__GD.new_vertex_property("string")
        self.__dictionary = dict()
        self.__lost_nodes = []
        pos = []
        for i in range(dim):
            pos.append(float(0.0))
        self.add_vertex(pos, color="green")
        self.expand_lattice(pos)
    
    def increase_size(self, size=1):
        self.__size+=size
    
    # add to the dictionary that maps coordinates to vertex number
    def add_to_dict(self, point, vertex_index):
        self.__dictionary[tuple(point)] = int(vertex_index)
        self.__dictionary[int(vertex_index)] = tuple(point)
        self.increase_size()
        
    def get_from_dictionary(self, key):
        if type(key) is int:
            return self.__dictionary[key]
        return self.__dictionary[tuple(key)]
    
    def get_color_of_node(self, pos):
        return self.__colors[self.get_from_dictionary(tuple(pos))]
    
    def get_valid_neighbors(self, pos, color):
                
        valid_neighbors = []
        
        # later will add check to make sure the neighbor is not the neighbor
        # of an already taken node
        
        for p in [right(pos), upper_right(pos), upper_left(pos), left(pos), lower_left(pos), lower_right(pos)]:
            if color == self.get_color_of_node(p):
                valid_neighbors.append(tuple(p))   
        return valid_neighbors
            
    
    def is_lost_node(self, node_pos):
        node_pos = tuple(node_pos)
        if node_pos in self.__lost_nodes: return True
        return False
    
    # expand the lattice around a certain point
    def expand_lattice(self, pos):
        
        # right node
        r = right(pos)
        rr = right(r)
        if tuple(rr) in self.__dictionary and self.get_color_of_node(tuple(rr)) == "green":
            print("HELLOOOOO")
            flag, r = self.add_vertex(r, color="maroon")
            #self.change_node_color(r, color="maroon")
        else:
            flag, r = self.add_vertex(r)
        self.connect(pos, r)
        
        # upper right node
        flag, ur = self.add_vertex(upper_right(pos))
        self.connect(pos, ur)
        
        # upper left node
        flag, ul = self.add_vertex(upper_left(pos))
        self.connect(pos, ul)
        
        # left node
        flag, l = self.add_vertex(left(pos))
        self.connect(pos, l)
        
        # lower left node
        flag, ll = self.add_vertex(lower_left(pos))
        self.connect(pos, ll)
        
        # lower right node
        flag, lr = self.add_vertex(lower_right(pos))
        self.connect(pos, lr)  
        
        # connect the outer boundary
        self.connect(r, ur)
        self.connect(ur, ul)
        self.connect(ul, l)
        self.connect(l, ll)
        self.connect(ll, lr)
        self.connect(lr, r)
        
    def change_node_color(self, pos, color="green"):
        self.__colors[self.get_from_dictionary(pos)] = color
    
    def connect(self, pos1, pos2):
        flag = not self.is_lost_node(pos1)
        # check for node
        if not self.cfn(pos2) and flag:
            flag, pos = self.add_vertex(pos2)
            
        # check for edge
        if flag and not self.cfe(pos1, pos2):    
            self.__GD.add_edge(self.get_vertex(pos1), self.get_vertex(pos2))
        else:
            print("STOPPED YOU!! :D")
        
    def add_vertex(self, pos, color="orange"):
        if self.is_lost_node(pos):
            return False, pos
        if not self.cfn(pos):
            v = self.__GD.add_vertex()
            self.add_to_dict(tuple(pos), v)
            self.__pos[v] = pos
            self.__colors[v] = color
        return True, pos
    
    def del_vertex(self, pos):
        pos = tuple(pos)
        pos_index = self.__dictionary.pop(pos, None)
        
        # if the vertex we are deleting was there
        if pos_index is not None:            
            last_index = self.get_last_index()
            last_node = self.__dictionary.pop(last_index)
            self.__dictionary.pop(last_node)
            self.add_to_dict(last_node, pos_index)
            self.increase_size(size=-1)
    
            self.__lost_nodes.append(pos)
            self.__GD.remove_vertex(pos_index, fast=True)
            
            # has to be -2 ...adding to the dictionary above increments size
            self.increase_size(size=-1)
            last_index = self.get_last_index()
            last_node = self.get_from_dictionary(last_index)
        else:
            print("NOOOOO")
            
    # take-over of node at pos2 by node at pos1
    def take_over_node(self, pos1, pos2):
        self.expand_lattice(pos2)
        i = self.get_from_dictionary(pos2)
        neighbors = self.__GD.get_out_neighbors(i)
        for n in neighbors:
            self.connect(pos1, self.get_from_dictionary(int(n)))
        self.del_vertex(pos2)

    # get dictionary method
    def get_dictionary(self):
        return self.__dictionary
    
    # get size method
    def get_size(self):
        return self.__size
    
    # get last index method which is the size minus 1
    def get_last_index(self):
        return self.__size - 1
          
    # get vertex at pos
    def get_vertex(self, pos):
        return self.__GD.vertex(self.get_from_dictionary(pos))
    
    def get_lost_nodes(self):
        return self.__lost_nodes
    
    # cfn = check for node
    def cfn(self, pos):
        if tuple(pos) in self.__dictionary:
            return True
        else:
            return False
        
    # cfe = check for edge
    def cfe(self, pos1, pos2):
        #try:
        neighbors = self.__GD.get_out_neighbors(self.get_from_dictionary(pos1))
        if self.get_from_dictionary(pos2) not in neighbors and tuple(pos1) != tuple(pos2):
            return False
        else:
            return True
        #except KeyError:
        #    return True
        
    # display the graph for the eyes to see  
    def display(self):
        #gt.graph_draw(self.__GD, pos=self.__pos, vertex_text=self.__GD.vertex_index, vertex_fill_color=self.__colors, vertex_shape="pentagon", vertex_font_size=12,
        #    output_size=self.__outputsize)
        gt.graph_draw(self.__GD, pos=self.__pos, vertex_fill_color=self.__colors, vertex_shape="pentagon", vertex_font_size=12,
            output_size=self.__outputsize)
        