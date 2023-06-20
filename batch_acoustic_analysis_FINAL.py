# -*- coding: utf-8 -*-
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
dirName = "/Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data"
#set up lists that will tell us which phone to look for in each file
s_words = ['soap', 'safe', 'seam', 'sob','soup']
r_words = ['rope', 'rob', 'roof', 'reef', 'ray']
s_data = []
r_data = []

#load csv with speaker data into python
os.chdir(dirName.replace("Production_Data",""))
pidf = pd.read_csv('Participant_Info.csv', usecols = ['STUDY_ID', 'GENDER'])

for sj in range(1,17):
    #set working directory for current subject
    subj = "S" + str(sj)
    subj_idx = pidf.index[pidf['STUDY_ID'] == subj]
    #get subject gender information
    gender = pidf['GENDER'][subj_idx[0]]
    os.chdir(dirName + "/" + subj + "/")
    #import each aligned TextGrid in turn for processing
    for txtgrd in glob.glob("aligned_textgrids/*.TextGrid"):
        print("Processing {}...".format(txtgrd))
        t = tgt.read_textgrid(txtgrd)
        phone_tier = t.get_tier_by_name('phones')
        word_tier = t.get_tier_by_name('words')
        
        #Procedure if fricative in file
        if any(x in txtgrd for x in s_words):
            s_instance = phone_tier.get_annotations_with_text("S")
            s = s_instance[0]
            startTime = s.start_time
            endTime = s.end_time
            wrd_instance = word_tier.get_annotations_by_time(endTime)
            w = wrd_instance[0]
            wrd = w.text
            #calculate middle 50 ms of fricative
            midpoint = startTime + ((endTime - startTime)/2)
            spliceStart = midpoint - 0.025
            spliceEnd = midpoint + 0.025
            #load the wav file associated with that text grid
            wavFile = txtgrd.replace("TextGrid", "wav")
            wavFile = wavFile.replace("aligned_textgrids/", "")
            sound = parselmouth.Sound(wavFile)    
            #import praat and get spectral measurements
            sound_part = sound.extract_part(from_time = spliceStart, to_time = spliceEnd)
            sound_part = call(sound_part, "Filter (stop Hann band)", 0, 500, 100)
            sound_spect = sound_part.to_spectrum()
            #sound_spect2 = call(sound_spect, "Filter (stop Hann band)", 0, 500, 100)
            cog = call(sound_spect, "Get centre of gravity", 2)
            kurt = sound_spect.get_kurtosis()
            standev = call(sound_spect, "Get standard deviation", 2)
            skew = call(sound_spect, "Get skewness", 2)
            s_data.append([subj, gender, "s", wrd, startTime, spliceStart, endTime, spliceEnd, cog, standev, skew, kurt])
            
        #Procedure if rhotic is target in file
        elif any(x in txtgrd for x in r_words):
            r_instance = phone_tier.get_annotations_with_text("R")
            r = r_instance[0]
            #calculate time points at which to extract formants (0, 25, 50, 75 and 100% of segment)
            startTime = r.start_time
            endTime = r.end_time
            wrd_instance = word_tier.get_annotations_by_time(endTime)
            w = wrd_instance[0]
            wrd = w.text
            midpoint = startTime + ((endTime - startTime)/2)
            quarter = midpoint - ((midpoint - startTime)/2)
            threequarters = midpoint + ((endTime - midpoint)/2)
            #load the wav file associated with that text grid
            wavFile = txtgrd.replace("TextGrid", "wav")
            wavFile = wavFile.replace("aligned_textgrids/", "")
            sound = parselmouth.Sound(wavFile)
            #generate formant object w/parameters based on subject gender
            if gender == "M" or gender == "TM": 
                sound_formant = call(sound, "To Formant (burg)", 0, 5, 5000, 0.25, 50)
            else:
                sound_formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.25, 50)
            F1Start = sound_formant.get_value_at_time(1, startTime)
            F1End = sound_formant.get_value_at_time(1, endTime)
            F1Mid = sound_formant.get_value_at_time(1, midpoint)
            F125 = sound_formant.get_value_at_time(1, quarter)
            F175 = sound_formant.get_value_at_time(1, threequarters)
            F2Start = sound_formant.get_value_at_time(2, startTime)
            F2End = sound_formant.get_value_at_time(2, endTime)
            F2Mid = sound_formant.get_value_at_time(2, midpoint)
            F225 = sound_formant.get_value_at_time(2, quarter)
            F275 = sound_formant.get_value_at_time(2, threequarters)
            F3Start = sound_formant.get_value_at_time(3, startTime)
            F3End = sound_formant.get_value_at_time(3, endTime)
            F3Mid = sound_formant.get_value_at_time(3, midpoint)
            F325 = sound_formant.get_value_at_time(3, quarter)
            F375 = sound_formant.get_value_at_time(3, threequarters)
            F4Start = sound_formant.get_value_at_time(4, startTime)
            F4End = sound_formant.get_value_at_time(4, endTime)
            F4Mid = sound_formant.get_value_at_time(4, midpoint)
            F425 = sound_formant.get_value_at_time(4, quarter)
            F475 = sound_formant.get_value_at_time(4, threequarters)
            r_data.append([subj, gender, "r", wrd, startTime, endTime, 
                           F1Start, F125, F1Mid, F175, F1End, 
                           F2Start, F225, F2Mid, F275, F2End, 
                           F3Start, F325, F3Mid, F375, F3End, 
                           F4Start, F425, F4Mid, F475, F4End])
s_data = pd.DataFrame(s_data)
s_data.to_csv('S_production_data.csv')
r_data = pd.DataFrame(r_data)
r_data.to_csv('R_production_data.csv')
