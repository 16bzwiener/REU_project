#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:10:27 2018

@author: benz
"""

import graph_tool.all as gt
from pathlib import Path

rootdir = Path('../25%Data')
# Return a list of regular files only, not directories
file_list = [str(f) for f in rootdir.glob('*') if f.is_file()]

# For absolute paths instead of relative the current dir
file_list_abs = [f for f in rootdir.resolve().glob('*') if f.is_file()]

accum = 0
hundreds = 0
thousands = 0
tenthousands = 0
hundthousands = 0

for f in file_list:
    g2 = gt.load_graph(f)

    #print((g2.graph_properties["position_list"].getSteps()))
    
    length = len(g2.graph_properties["position_list"].getList())
    
    accum += length
    
    if length < 100:
        hundreds+=1
    elif length < 1000:
        thousands+=1
    elif length < 10000:
        tenthousands+=1
    else:
        hundthousands+=1
    
    
    
    gt.graph_draw(g2, 
                  pos=g2.vertex_properties["vertex positions"], 
                  vertex_fill_color=g2.vertex_properties["vertex colors"],
                  edge_color=g2.edge_properties["edge colors"],
                  vertex_shape="hexagon", 
                  vertex_font_size=12,
                  output_size=(500,500)
                  #vertex_text=self.__Graph.vertex_index
                  )
    
'''    

print("Average Length: ", accum/len(file_list))
print("Less than 100: ", hundreds)
print("Less than 1000: ", thousands)
print("Less than 10000: ", tenthousands)
print("More than 10000: ", hundthousands)

rootdir = Path('../30%Data')
# Return a list of regular files only, not directories
file_list = [str(f) for f in rootdir.glob('*') if f.is_file()]

# For absolute paths instead of relative the current dir
file_list_abs = [f for f in rootdir.resolve().glob('*') if f.is_file()]

accum = 0
hundreds = 0
thousands = 0
tenthousands = 0
hundthousands = 0

for f in file_list:
    g2 = gt.load_graph(f)

    #print((g2.graph_properties["position_list"].getSteps()))
    
    length = len(g2.graph_properties["position_list"].getList())
    
    accum += length
    
    if length < 100:
        hundreds+=1
    elif length < 1000:
        thousands+=1
    elif length < 10000:
        tenthousands+=1
    else:
        hundthousands+=1
    
    
    
    gt.graph_draw(g2, 
                  pos=g2.vertex_properties["vertex positions"], 
                  vertex_fill_color=g2.vertex_properties["vertex colors"],
                  edge_color=g2.edge_properties["edge colors"],
                  vertex_shape="hexagon", 
                  vertex_font_size=12,
                  output_size=(500,500)
                  #vertex_text=self.__Graph.vertex_index
                  )
    
    

print("Average Length: ", accum/len(file_list))
print("Less than 100: ", hundreds)
print("Less than 1000: ", thousands)
print("Less than 10000: ", tenthousands)
print("More than 10000: ", hundthousands)

rootdir = Path('../35%Data')
# Return a list of regular files only, not directories
file_list = [str(f) for f in rootdir.glob('*') if f.is_file()]

# For absolute paths instead of relative the current dir
file_list_abs = [f for f in rootdir.resolve().glob('*') if f.is_file()]

accum = 0
hundreds = 0
thousands = 0
tenthousands = 0
hundthousands = 0

for f in file_list:
    g2 = gt.load_graph(f)

    #print((g2.graph_properties["position_list"].getSteps()))
    
    length = len(g2.graph_properties["position_list"].getList())
    
    accum += length
    
    if length < 100:
        hundreds+=1
    elif length < 1000:
        thousands+=1
    elif length < 10000:
        tenthousands+=1
    else:
        hundthousands+=1
    
    
    
    #gt.graph_draw(g2, 
    #              pos=g2.vertex_properties["vertex positions"], 
    #              vertex_fill_color=g2.vertex_properties["vertex colors"],
    #              edge_color=g2.edge_properties["edge colors"],
    #              vertex_shape="hexagon", 
    #              vertex_font_size=12,
    #              output_size=(500,500)
    #              #vertex_text=self.__Graph.vertex_index
    #              )
    
    

print("Average Length: ", accum/len(file_list))
print("Less than 100: ", hundreds)
print("Less than 1000: ", thousands)
print("Less than 10000: ", tenthousands)
print("More than 10000: ", hundthousands)

rootdir = Path('../40%Data')
# Return a list of regular files only, not directories
file_list = [str(f) for f in rootdir.glob('*') if f.is_file()]

# For absolute paths instead of relative the current dir
file_list_abs = [f for f in rootdir.resolve().glob('*') if f.is_file()]

accum = 0
hundreds = 0
thousands = 0
tenthousands = 0
hundthousands = 0

for f in file_list:
    g2 = gt.load_graph(f)

    #print((g2.graph_properties["position_list"].getSteps()))
    
    length = len(g2.graph_properties["position_list"].getList())
    
    accum += length
    
    if length < 100:
        hundreds+=1
    elif length < 1000:
        thousands+=1
    elif length < 10000:
        tenthousands+=1
    else:
        hundthousands+=1
    
    
    
    #gt.graph_draw(g2, 
    #              pos=g2.vertex_properties["vertex positions"], 
    #              vertex_fill_color=g2.vertex_properties["vertex colors"],
    #              edge_color=g2.edge_properties["edge colors"],
    #              vertex_shape="hexagon", 
    #              vertex_font_size=12,
    #              output_size=(500,500)
    #              #vertex_text=self.__Graph.vertex_index
    #              )
    
    

print("Average Length: ", accum/len(file_list))
print("Less than 100: ", hundreds)
print("Less than 1000: ", thousands)
print("Less than 10000: ", tenthousands)
print("More than 10000: ", hundthousands)
#'''