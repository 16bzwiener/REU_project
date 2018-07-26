#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:48:21 2018

@author: benz
"""

import matplotlib.pyplot as plt
import graph_tool.all as gt
import sys
import numpy as np

for num in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
    #g2.edges()
    g2 = gt.load_graph("forPresentation_expansion_" + num + ".xml.gz")
    dic = dict()
    for i, v in enumerate(g2.properties[('v', 'vertex positions')]):
        dic[i] = v
    dim = 13
    shiftx = 5
    shifty = 2
    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.set_ylim([-dim+shifty, dim+shifty])
    ax.set_xlim([-dim+shiftx, dim+shiftx])
    fig.add_axes(ax)
    
    #print(g2.properties.keys())
    
    for e in g2.edges():
        source = e.source()
        target = e.target()
        start = dic[source]
        end = dic[target]
        plt.plot([start[0], end[0]], [-start[1], -end[1]], color="orange", linewidth=1)
        
    
    for i in g2.graph_properties["position_list"].getList():
        start = np.array(i[0])
        #print(start)
        end = np.array(i[2])
        #print(end)
        plt.plot([start[0], end[0]], [-start[1], -end[1]], color="green", linewidth=3)
        
    for i, j in zip(g2.properties[('v', 'vertex positions')], g2.properties[('v', 'vertex colors')]):
        plt.plot(i[0], -i[1], color=j, marker='o', markersize=8)
    
    
        
    plt.savefig('p' + num + '.png', bbox_inches='tight', pad_inches = 0)
    plt.clf()
    
        
#fig = plt.plot([1,2,3,4])
#fig.show()
#plt.savefig("test.png", bbox_inches='tight')

