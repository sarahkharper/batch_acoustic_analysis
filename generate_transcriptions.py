#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:26:08 2021

@author: sarahharper
"""

import pandas as pd

df = pd.read_excel('/Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data/S6/S6_production_trials_transcription_list.xlsx', header = 0)

for row in df.index:
    print(row)
    with open (str(df.iloc[row]["subject"]) + "_" + df.iloc[row]["item"] + "_" + str(df.iloc[row]["repetition"]) + ".lab", "w") as fout:
        print(df.iloc[row]["text"], file = fout)