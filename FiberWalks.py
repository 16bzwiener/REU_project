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
lattice = HL.HexagonalLattice(color="orange", outputsize=(500,500))
lattice.set_node_color(pos=(0,0), color=root_color)
pos = (0,0)
valid = []

class BranchingFW:
    
    def __init__(self, steps=100, outputsize=(500,500), dim=2):
        self.__lattice = HL.HexagonalLattice(outputsize=outputsize)
        self.__pos = tuple(np.zeros(dim))
        self.__pos_list = [[self.__pos]]
        self.walk(steps)

    def direction(self, pos1, pos2):
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
            
    def step(self):
        return 1
            
    def walk(self):
        return 1
    
walk = BranchingFW()

'''
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