#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 10:01:52 2018

@author: benz
"""

class DataForRoot:
    
    def __init__(self, posList, probability, steps):
        self.__posList = posList
        self.__probability = probability
        self.__steps = steps
        
    def getList(self):
        return self.__posList
    
    def getProbability(self):
        return self.__probability
    
    def getSteps(self):
        return self.__steps