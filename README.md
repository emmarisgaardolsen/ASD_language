# ASD_language
This repository contains code for extracting acoustic features from a speaker diarised corpus of US child-caregiver interactions. The dataset comprises two distinct groups: children diagnosed with Autism Spectrum Disorder (ASD) and neurotypical children.


## Steps

### Step 1: Set up virtual environment
```
bash setup_venv.sh
```

### Step 2: Activate virtual environment 
```
source venv/bin/activate
```

### Step 3: 


## Project Organisation
The data was structured in the following manner, and running the code requires you to have the data organised in a corresponding folder structure. The data is not included in this repository.


```
├── data                                         Not in repository
│   ├── CDS_wavs 
│   ├── CDS_wavs 
│           └── childname_Visit_X.wav
│           └── ...
│       └── f0_extracted
│           └── childname_Visit_X_f0.txt         Extracted fundamental frequency
│           └── ...
│       └── textgrid
│           └── childname_Visit_X.TextGrid       TextGrid files from Praat
│           └── ...
│       └── TurnTakingData.csv                   Diarised corpus
│   └── src 
│       └── opensmile_features.ipynb             Notebook for extracting eGeMAPSv02 features with opensmile 
│       └── fundamental_freq.py                  Script for summarising fundamental frequency
│       └── vowels.py                            Script for extracting articulation rate

├── outputs                                      Outputs from running the scripts
├── README.md
├── requirements.txt
├── setup.sh
├── get_ipykernel.sh
```
