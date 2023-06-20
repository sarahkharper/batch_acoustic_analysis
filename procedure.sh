#!/bin/bash
subj="3611028"

#relabel mp3 files for subj
cd /Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data/mp3s

for i in *.mp3; do sox "$i" "$(basename -s .mp3 "$i").wav";done

cd /Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data

#remember to change subj variable in rename.sh before running
sh rename.sh

#remember to save copy of generate_transcriptions to directory and change path in file. And update excel sheet for speaker.
conda activate mython
python generate_transcriptions 
conda deactivate

conda activate aligner
mfa align /Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data/S23 /Users/sarahharper/Dropbox/My\ Mac\ \(Sarah’s\ MacBook\ Pro\)/Documents/MFA/pretrained_models/dictionary/librispeech-lexicon.txt english /Users/sarahharper/Dropbox/Research/Dissertation/Perception_Experiment/Data/Production_Data/S23/aligned_textgrids -c
conda deactivate
