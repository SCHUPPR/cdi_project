# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:10:27 2023

@author: Reece
"""

import pandas as pd

# CDI Project

# Loading Data

raw_df = pd.read_csv("cdi_data.csv", dtype={"DataValue":"object"})