#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:04:04 2018

@author: benz
"""

import numpy as np

sot = 2
#sot = np.sqrt(3)

# 2-D directions     
def right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([2,0]))

def left(point: np.ndarray) -> np.ndarray:
    return (point + np.array([-2,0]))

def upper_right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([1,-sot]))

def lower_right(point: np.ndarray) -> np.ndarray:
    return (point + np.array([1,sot]))

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

def two_d_expansion(pos, settings=0):
    
    arr = np.array(pos)
    
    moves = []
    if settings == 0 or arr[1] >= 50:
        moves = [right(pos), right(pos), upper_right(pos), upper_left(pos), left(pos), left(pos), 
             lower_left(pos), lower_left(pos), lower_left(pos), lower_right(pos), lower_right(pos), lower_right(pos)]
    elif arr[1] == 0:
        moves = [lower_left(pos), lower_right(pos)]
    elif arr[1] < 50:
        moves = [right(pos), right(pos), left(pos), left(pos), 
             lower_left(pos), lower_left(pos), lower_left(pos), lower_right(pos), lower_right(pos), lower_right(pos)]
    
    vertice_pos = []
    
    for m in moves:
        vertice_pos.append(tuple(m))
    
    edges = []
    
    for p in vertice_pos:
        edges.append([pos, p])
    
    length = len(vertice_pos)
    for i in range(length):
        if i < length-1:
            edges.append([vertice_pos[i], vertice_pos[i+1]])
        else:
            edges.append([vertice_pos[0], vertice_pos[length - 1]])
    
    return vertice_pos, edges

def two_d_contraction(pos):
    randnum = np.random.randint(3)
    if randnum == 0:
        return [right(pos), left(pos)]
    elif randnum == 1:
        return [upper_right(pos), lower_left(pos)]
    else:
        return [lower_right(pos), upper_left(pos)]
    
def surrounding(pos, dim=2, setting=0):
    if dim == 2:
        return two_d_expansion(pos, setting)
    
def contraction(pos, dim=2):
    if dim == 2:
        return two_d_contraction(pos)