#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:11:03 2018

@author: benz
"""

import numpy as np
import graph_tool.all as gt

class HexagonalLattice2D:
    
    # construct the lattice :D
    def __init__(self, pos, outputsize=(500,500)):
        self.__outputsize = outputsize
        self.__size = 0
        self.__Graph = gt.Graph(directed=False)
        self.__pos = self.__GD.new_vertex_property("vector<double>")
        self.__colors = self.__GD.new_vertex_property("string")
        self.__dictionary = dict()
        self.__lost_nodes = set()
        self.add_vertex(pos, color="green")
        self.expand_lattice(pos)
      
    # add a vertex (node) at the entered position with a certain color
    def add_vertex(self, pos, color="orange"):
        # if it is a lost node that was taken over do not add a node
        if self.is_lost_node(pos):
            return False, pos
        # if a node is not there, add one
        if not self.cfn(pos):
            v = self.__Graph.add_vertex()
            self.add_to_dict(tuple(pos), v)
            self.__pos[v] = pos
            self.__colors[v] = color
        return True, pos
    
    # add to the dictionary that maps coordinates to vertex number
    def add_to_dict(self, point, vertex_index):
        self.__dictionary[tuple(point)] = int(vertex_index)
        self.__dictionary[int(vertex_index)] = tuple(point)
        self.increase_size()
    
    # what does my key map to? RETURN IT!    
    def get_from_dictionary(self, key):
        if type(key) is int:
            return self.__dictionary[key]
        return self.__dictionary[tuple(key)]
    
    # what color is the node here? RETURN IT!
    def get_color_of_node(self, pos):
        return self.__colors[self.get_from_dictionary(tuple(pos))]
    
    # does this position contain a lost node?
    def is_lost_node(self, node_pos):
        node_pos = tuple(node_pos)
        if node_pos in self.__lost_nodes: return True
        return False
    
    # contribute to the set of lost nodes
    def add_lost_node(self, node_pos):
        self.__lost_nodes.add(node_pos)
        
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
        
    # display the graph for the eyes to see  
    def display(self):
        #gt.graph_draw(self.__GD, pos=self.__pos, vertex_text=self.__GD.vertex_index, vertex_fill_color=self.__colors, vertex_shape="pentagon", vertex_font_size=12,
        #    output_size=self.__outputsize)
        gt.graph_draw(self.__GD, pos=self.__pos, vertex_fill_color=self.__colors, vertex_shape="pentagon", vertex_font_size=12,
            output_size=self.__outputsize)
    
    # increases size by one if no parameters added
    # if parameter is entered changes size by that much
    def increase_size(self, size=1):
        self.__size+=size