#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 16:07:55 2018

@author: benz
"""

import HexagonalLattice as HL
import FiberWalks as FW
import numpy as np

state = np.random.get_state()

FW.BranchingFW(steps=0)

np.random.set_state(state)

FW.BranchingFW(steps=1)

np.random.set_state(state)

FW.BranchingFW(steps=2)

np.random.set_state(state)

FW.BranchingFW(steps=3)