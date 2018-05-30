#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:03:57 2018

@author: benz
"""

class Point():
    
    def __init__(self, dim=2, coord=None):
        if coord is not None:
            self.__coord = tuple(coord)
        else:
            pos = []
            for i in range(dim):
                pos.append(float(0.0))
            self.__coord = tuple(pos)
            
    def get_coord(self):
        return self.__coord
            
p = Point(coord=(5, 0.))

print(p.get_coord())