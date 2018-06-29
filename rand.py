#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 14:01:23 2018

@author: benz
"""

import numpy as np

state = np.random.get_state()

for i in range(6):
    print(np.random.randint(10))
    
print("HI")
    
np.random.set_state(state)

for i in range(6):
    print(np.random.randint(10))