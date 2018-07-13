#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:48:21 2018

@author: benz
"""

import graph_tool.all as gt

g2 = gt.load_graph("test.xml.gz")

print(g2.graph_properties["position_list"].getProbability())

gt.graph_draw(g2, 
              pos=g2.vertex_properties["vertex positions"], 
              vertex_fill_color=g2.vertex_properties["vertex colors"],
              edge_color=g2.edge_properties["edge colors"],
              vertex_shape="hexagon", 
              vertex_font_size=12,
              output_size=(500,500)
              #vertex_text=self.__Graph.vertex_index
              )