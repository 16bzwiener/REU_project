#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:04:04 2018

@author: benz
"""

import numpy as np

sot = np.sqrt(3)

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

def Two_D_Expansion(pos):
    return [right(pos), upper_right(pos), upper_left(pos), 
            left(pos), lower_left(pos), lower_right(pos)]