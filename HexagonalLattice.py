#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:11:03 2018

@author: benz
"""

import numpy as np
import graph_tool.all as gt
import LatticeDirections as LD
import time

class HexagonalLattice:
    
    # construct the lattice :D
    def __init__(self, pos=(0,0), outputsize=(500,500), vertex_color="orange", dim=2):
        
        # fields of this class include outputsize, size, Graph, pos vertex prop,
        # colors vertex property, dictionary (dict), lost nodes (set), 
        # main color and dim 
        self.__outputsize = outputsize
        self.__size = 0
        self.__Graph = gt.Graph(directed=False)
        self.__pos = self.__Graph.new_vertex_property("vector<double>")
        self.__vertex_colors = self.__Graph.new_vertex_property("string")
        self.__edge_colors = self.__Graph.new_edge_property("vector<double>")
        self.__dictionary = dict()
        self.__lost_nodes = set()
        self.__main_color = vertex_color
        self.__dim = dim
        
        # add the initial vertex and expand the lattice
        self.add_vertex(pos)
        self.expand_lattice(pos)
      
    # add a vertex (node) at the entered position with a certain color
    def add_vertex(self, pos):
        
        # if it is a lost node that was taken over do not add a node
        if self.is_lost_node(pos):
            return False, pos
        
        # if a node is not there, add one
        if not self.cfn(pos):
            
            # add a vertex to the graph, add the pos and vertex index to dict
            v = self.__Graph.add_vertex()
            self.add_to_dict(tuple(pos), v)
            
            # set the coordinate pos and color for the node
            self.__pos[v] = pos
            self.__vertex_colors[v] = self.__main_color
        
        # return true since there is a node there
        return True, pos
    
    # add to the dictionary that maps coordinates to vertex number
    # first parameter is the coordinate point
    # second parameter is the index of the vertice
    def add_to_dict(self, point, vertex_index):
        
        # map a coordinate point to a index
        self.__dictionary[tuple(point)] = int(vertex_index)
        
        # map the vertex index to a coordinate point
        self.__dictionary[int(vertex_index)] = tuple(point)
        
        # increase the size of the graph
        self.increase_size()
    
    # what does my key map to? RETURN IT!    
    def get_from_dictionary(self, key):
        
        # if the key entered was an int return the coordinate it is paired with
        if type(key) is int:
            return self.__dictionary[key]
        
        # if the key wasn't an int, it was a coordinate...return the index
        return self.__dictionary[tuple(key)]
    
    # what color is the node here? RETURN IT!
    def get_color_of_node(self, pos):
        if tuple(pos) in self.__dictionary:
            return self.__vertex_colors[self.get_from_dictionary(tuple(pos))]
        
        return None
    
    # get the color of the edge
    def get_color_of_edge(self, pos1, pos2): 
        return self.__edge_color[self.get_edge(pos1,pos2)]
    
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
        return self.__Graph.vertex(self.get_from_dictionary(pos))
    
    # get edge that connects the two positions
    def get_edge(self, pos1, pos2):
        return self.__Graph.edge(self.get_from_dictionary(pos1), self.get_from_dictionary(pos2))
    
    # get lost nodes set
    def get_lost_nodes(self):
        return self.__lost_nodes
    
    def get_neighbors(self, pos):
        indices = list(self.__Graph.get_out_neighbors(self.get_from_dictionary(pos)))
        neigh = []
        for n in indices:
            neigh.append(self.get_from_dictionary(int(n)))
        return indices, neigh
    
    # does this position contain a lost node?
    def is_lost_node(self, node_pos):
        
        # get the node pos
        node_pos = tuple(node_pos)
        
        # if the node is a lost node return true, else return false
        if node_pos in self.__lost_nodes: return True
        return False
    
    # contribute to the set of lost nodes
    def add_lost_node(self, node_pos):
        self.__lost_nodes.add(node_pos)
    
    # get direction vector
    def get_direction_vector(self, pos1, pos2):
        m = np.matrix([[1, 0], [0, (3/4)**(1/2)]])
        dif = np.subtract(pos2, pos1)
        dif = np.array(dif*m)[0]
        mag = (dif[0]**2 + dif[1]**2)**(1/2)
        soe = sum(np.absolute(dif))
        direction = dif/soe
        return direction
    
    # connect two vertices (nodes) with an edge
    def connect(self, pos1, pos2):
        
        # see if it is a lost node
        lost_node = not self.is_lost_node(pos1)
        
        # check for node
        if not self.cfn(pos2) and lost_node:
            lost_node, pos = self.add_vertex(pos2)
            
        # check for edge, if there isn't one add an edge
        if lost_node and not self.cfe(pos1, pos2):    
            self.__edge_colors[self.__Graph.add_edge(self.get_vertex(pos1), self.get_vertex(pos2))] = (.8, .5, 0, .5)
        else:
            print("STOPPED YOU!! :D")
            
    # cfe = check for edge
    def cfe(self, pos1, pos2):
        
        # find the neighbors of vertex at pos 1
        neighbors = self.__Graph.get_out_neighbors(self.get_from_dictionary(pos1))
        
        # if the vertex at pos 2 is a neighbor and pos 1 is not equal to pos 2
        if self.get_from_dictionary(pos2) not in neighbors and tuple(pos1) != tuple(pos2):
            return False
        else:
            return True
        
    # cfn = check for node
    def cfn(self, pos):
        
        # if pos is in the dictionary return true: else return false
        if tuple(pos) in self.__dictionary:
            return True
        else:
            return False
        
    # set the color of the node
    def set_node_color(self, pos, color=None):
        if tuple(pos) in self.__dictionary:
            # if no color is inserted, use the main color
            if color is None:
                color = self.__main_color
                
            self.__vertex_colors[self.get_from_dictionary(pos)] = color
            
    def set_edge_color(self, pos1, pos2, color):
        e = self.__Graph.edge(self.get_vertex(pos1), self.get_vertex(pos2))
        self.__edge_colors[e] = color
        
    # expand the lattice around a certain point
    def expand_lattice(self, pos):
        
        # get the surrounding vertices and the needed edges
        surrounding, edges =  LD.surrounding(pos=pos, dim=self.__dim)
        
        # create the new vertices
        for p in surrounding:
            flag, p = self.add_vertex(p)
        
        # connect all the needed edges
        for e in edges:
            self.connect(e[0], e[1])
            
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
    
            self.__lost_nodes.add(pos)
            self.__Graph.remove_vertex(pos_index, fast=True)
            
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
        neighbors = self.__Graph.get_out_neighbors(i)
        for n in neighbors:
            self.connect(pos1, self.get_from_dictionary(int(n)))
        self.del_vertex(pos2)
    
    # display the graph for the eyes to see  
    def display(self, save=0, outputsize=(500,500)):
        #gt.graph_draw(self.__Graph, pos=self.__pos, vertex_text=self.__Graph.vertex_index, vertex_fill_color=self.__colors, vertex_shape="pentagon", vertex_font_size=12,
        #    output_size=self.__outputsize)
        #gt.graph_draw(self.__Graph, pos=self.__pos, vertex_fill_color=self.__colors, vertex_shape="hexagon", vertex_font_size=12,
        #    output_size=self.__outputsize, output="../20steps.png")
        if save == 0:
            gt.graph_draw(self.__Graph, 
                      pos=self.__pos, 
                      vertex_fill_color=self.__vertex_colors,
                      edge_color=self.__edge_colors,
                      vertex_shape="hexagon", 
                      vertex_font_size=12,
                      output_size=outputsize,
                      vertex_text=self.__Graph.vertex_index)
        else:
            gt.graph_draw(self.__Graph, 
                      pos=self.__pos, 
                      vertex_fill_color=self.__vertex_colors,
                      edge_color=self.__edge_colors,
                      vertex_shape="hexagon", 
                      vertex_font_size=12,
                      output_size=outputsize,
                      output="../contract.png",
                      vertex_text=self.__Graph.vertex_index)
    
    # increases size by one if no parameters added
    # if parameter is entered changes size by that much
    def increase_size(self, size=1):
        self.__size+=size
'''        
root_color = "green"        
lattice = HexagonalLattice(color="orange", outputsize=(500,500))
lattice.set_node_color(pos=(0,0), color=root_color)
pos = (0,0)
valid = []

def direction(pos1, pos2):
    pos1 = tuple(pos1)
    pos2 = tuple(pos2)
    pos3 = tuple(np.absolute(np.subtract(pos1, pos2)))
    if pos3 == (2,0):
        # it is right!
        if tuple(np.add(pos1, (2,0))) == pos2:
            return LD.right_shared(pos1)
        # it is left
        else:
            return LD.left_shared(pos1)
    else:
        if tuple(np.add(pos1, (1,2))) == pos2:
            return LD.lower_right_shared(pos1)
        elif tuple(np.add(pos1, (1,-2))) == pos2:
            return LD.upper_right_shared(pos1)
        elif tuple(np.add(pos1, (-1,2))) == pos2:
            return LD.lower_left_shared(pos1)
        else:
            return LD.upper_left_shared(pos1)

def find_off_limits(pos):
    
    color = lattice.get_color_of_node(pos)

    surround = [LD.right(pos), LD.upper_right(pos), LD.upper_left(pos), LD.left(pos), 
             LD.lower_left(pos), LD.lower_right(pos)]

    p = LD.right(LD.right(pos))
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")        
    
    p = LD.upper_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")

    p = LD.upper_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")
    
    p = LD.left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[1]) != root_color:
            lattice.set_node_color(surround[1], "maroon")
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")

    p = LD.left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")
    
    p = LD.lower_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[2]) != root_color:
            lattice.set_node_color(surround[2], "maroon")
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
    
    p = LD.lower_left(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
    
    p = LD.lower_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[3]) != root_color:
            lattice.set_node_color(surround[3], "maroon")
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")

    p = LD.lower_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")
    
    p = LD.right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[4]) != root_color:
            lattice.set_node_color(surround[4], "maroon")
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")

    p = LD.right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")
    
    p = LD.upper_right(p)
    if lattice.get_color_of_node(p) == color:
        if lattice.get_color_of_node(surround[5]) != root_color:
            lattice.set_node_color(surround[5], "maroon")
        if lattice.get_color_of_node(surround[0]) != root_color:
            lattice.set_node_color(surround[0], "maroon")

def step(pos, valid_prev):
        
    valid, _ = LD.surrounding(pos, setting=1)
    for i in valid[:]:
        if lattice.get_color_of_node(pos=i) != "orange" or i in valid_prev:
            valid.remove(i)
    
    if len(valid) > 0:
        rand = np.random.randint(len(valid))
        pos = valid[rand]
        lattice.set_node_color(pos=pos, color=root_color)
        lattice.expand_lattice(pos)
        
    find_off_limits(pos)
        
    return tuple(pos), valid    

def contraction(pos):
    list = LD.contraction(pos)
    for p in list:
        lattice.take_over_node(pos, p)
        
posList = [pos]
currentTips = [pos]

# this branches
for i in range(5):
    for p in currentTips[:]:
        currentTips.remove(p)
        rand = np.random.randint(100)
        pos, valid = step(p, valid)
        posList.append(pos)
        currentTips.append(pos)
        if rand > 45 and rand < 55 and posList[i] != posList[i+1]:
            currentTips.append(p)
        time.sleep(2)
        lattice.display()
    if len(currentTips) == 0:
        break
    print(i)

lattice.display()
'''