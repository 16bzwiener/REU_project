#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 16:07:55 2018

@author: benz
"""

import HexagonalLattice as HL
import FiberWalks as FW
import numpy as np
import sys

# should be a string...will have ".xml.gz" added to the end of it
filename = sys.argv[1]

# branching probability
probability = int(sys.argv[2])

# number of steps
steps = int(sys.argv[3])

FW.BranchingFW(steps=steps, prob=probability, filename=filename)