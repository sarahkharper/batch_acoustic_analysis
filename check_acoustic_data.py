#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 23:39:54 2021

@author: sarahharper
"""

"""
Spyder Editor

This is a temporary script file.
"""
#import sys
import os
import parselmouth
from parselmouth.praat import call
import glob
#import numpy as np
import pandas as pd
import tgt

#user_input = raw_input("Enter parent directory for files: ")
#assert os.path.exists(user_input), "No existing directory"
dirName = "/Users/sarahharper/Dropbox/Research/Quals/XRMB/mat"
#set up lists that will tell us which phone to look for in each file
#s_words = ['soap', 'safe', 'seam', 'sob','soup']
#r_words = ['rope', 'rob', 'roof', 'reef', 'ray']
s_data = []
r_data = []
#r_data = []

#load csv with speaker data into python
os.chdir(dirName)
pidf = pd.read_csv('all_data_acoustic_timepoints.csv', usecols = ['SUBJ', 'GENDER', 'PHONE', 'WORD', 'TASK', 'MID', 'BEGIN', 'ENDS'])

for sj in pidf.index:
    #set working directory for current subject
    subj = pidf['SUBJ'][sj]
    phone = pidf['PHONE'][sj]
    gender = pidf['GENDER'][sj]
    if phone == "S" or phone == "SH":
    #subj_idx = pidf.index[pidf['STUDY_ID'] == subj]
    #get subject gender information
        word = pidf['WORD'][sj]
        timeptRaw = pidf['MID'][sj]
        timept = timeptRaw/1000
        timeptBRaw = pidf['BEGIN'][sj]
        timeptB = timeptBRaw/1000
        timeptERaw = pidf['ENDS'][sj]
        timeptE = timeptERaw/1000
        task = pidf['TASK'][sj]
        #tracking_max = pidf['TRACKING_MAX'][subj_idx[0]]
        wavFile = subj + "_" + task + "_scaled.wav"
        print("Processing {}...".format(wavFile))
        #t = tgt.read_textgrid(txtgrd)
        #phone_tier = t.get_tier_by_name('phone')
        #word_tier = t.get_tier_by_name('word')
        
        #Procedure if fricative in file
        #phn_tms = phone_tier.get_annotations_by_time(timept)
        #phn = phn_tms[0]
        #p = phn.text
        #wavFile = txtgrd.replace("TextGrid", "wav")
        #wavFile = wavFile.replace("aligned_textgrids/", "")
        sound = parselmouth.Sound(wavFile)    
        #if p == phone:
           #  startTime = phn.start_time
           #  endTime = phn.end_time
           #  midpoint = startTime + ((endTime - startTime)/2)
           # #calculate middle 50 ms of fricative
           #  spliceStart = midpoint - 0.025
           #  spliceEnd = midpoint + 0.025
           #  #load the wav file associated with that text grid
           #  #import praat and get spectral measurements
           #  sound_part = sound.extract_part(from_time = spliceStart, to_time = spliceEnd)
           #  sound_part = call(sound_part, "Filter (stop Hann band)", 0, 500, 100)
           #  sound_spect = sound_part.to_spectrum()
           #  #sound_spect2 = call(sound_spect, "Filter (stop Hann band)", 0, 500, 100)
           #  cog_phn = call(sound_spect, "Get centre of gravity", 2)
           #  kurt_phn = sound_spect.get_kurtosis()
           #  standev_phn = call(sound_spect, "Get standard deviation", 2)
           #  skew_phn = call(sound_spect, "Get skewness", 2)
        timeptStart = timept - 0.025
        timeptEnd = timept + 0.025
        sound_part = sound.extract_part(from_time = timeptStart, to_time = timeptEnd)
        sound_part = call(sound_part, "Filter (stop Hann band)", 0, 500, 100)
        sound_spect = sound_part.to_spectrum()
        #sound_spect = call(sound_spect, "Filter (stop Hann band)", 0, 500, 100)
        cog_tm = call(sound_spect, "Get centre of gravity", 2)
        kurt_tm = sound_spect.get_kurtosis()
        standev_tm = call(sound_spect, "Get standard deviation", 2)
        skew_tm = call(sound_spect, "Get skewness", 2)
        s_data.append([subj, gender, phone, word, task, timeptRaw, timeptBRaw, timeptERaw, cog_tm, standev_tm, skew_tm, kurt_tm])
    elif phone == "L" or phone == "R":
        word = pidf['WORD'][sj]
        #get timepoints of interest
        timeptRaw = pidf['MID'][sj]
        timept = timeptRaw/1000
        timeptBRaw = pidf['BEGIN'][sj]
        timeptB = timeptBRaw/1000
        timeptERaw = pidf['ENDS'][sj]
        timeptE = timeptERaw/1000
        task = pidf['TASK'][sj]
        wavFile = subj + "_" + task + "_scaled.wav"
        print("Processing {}...".format(wavFile))
        sound = parselmouth.Sound(wavFile)
        if gender == 'F':
            sound_formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
            #Get F1 measurements
            F1Mid = sound_formant.get_value_at_time(1, timept)
            F1Start = sound_formant.get_value_at_time(1, timeptB)
            F1End = sound_formant.get_value_at_time(1, timeptE)
            F2Start = sound_formant.get_value_at_time(2, timeptB)
            F2End = sound_formant.get_value_at_time(2, timeptE)
            F2Mid = sound_formant.get_value_at_time(2, timept)
            F3Start = sound_formant.get_value_at_time(3, timeptB)
            F3End = sound_formant.get_value_at_time(3, timeptE)
            F3Mid = sound_formant.get_value_at_time(3, timept)
            F4Start = sound_formant.get_value_at_time(4, timeptB)
            F4End = sound_formant.get_value_at_time(4, timeptE)
            F4Mid = sound_formant.get_value_at_time(4, timept)
        else:
            sound_formant = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
            #Get F1 measurements
            F1Mid = sound_formant.get_value_at_time(1, timept)
            F1Start = sound_formant.get_value_at_time(1, timeptB)
            F1End = sound_formant.get_value_at_time(1, timeptE)
            F2Start = sound_formant.get_value_at_time(2, timeptB)
            F2End = sound_formant.get_value_at_time(2, timeptE)
            F2Mid = sound_formant.get_value_at_time(2, timept)
            F3Start = sound_formant.get_value_at_time(3, timeptB)
            F3End = sound_formant.get_value_at_time(3, timeptE)
            F3Mid = sound_formant.get_value_at_time(3, timept)
            F4Start = sound_formant.get_value_at_time(4, timeptB)
            F4End = sound_formant.get_value_at_time(4, timeptE)
            F4Mid = sound_formant.get_value_at_time(4, timept)
        r_data.append([subj, gender, phone, word, task, timeptRaw, timeptBRaw, timeptERaw,
                          F1Mid, F1Start, F1End, F2Mid, F2Start, F2End, F3Mid, F3Start,
                          F3End, F4Mid, F4Start, F4End])
s_data = pd.DataFrame(s_data)
s_data.columns = ['SUBJ', 'GENDER', "PHONE", 'WORD', 'TASK', 'MID', 'START', 'END', 
                  'CoG_MAXC', 'StDev_MAXC', 'Skewness_MAXC', 'Kurtosis_MAXC']
s_data.to_csv('Fricative_acoustic_data_checked_May23.csv')
r_data = pd.DataFrame(r_data)
r_data.columns = ['SUBJ', 'GENDER', 'PHONE', 'WORD', 'TASK', 'MID', 'START', 'END',
                  'F1Mid', 'F1Start', 'F1End', "F2Mid", 'F2Start', 'F2End',
                  'F3Mid', 'F3Start', 'F3End', 'F4Mid', 'F4Start', 'F4End']
r_data.to_csv('Liquid_acoustic_data_checked_May23.csv')
