# ASD_language
This repository contains code for extracting acoustic features from a speaker diarised corpus of US child-caregiver interactions. The dataset comprises a total of 77 children categorised into two distinct groups: children diagnosed with Autism Spectrum Disorder (ASD) and neurotypical children.

Each child has 4-6 recording sessions (.wav files) upon which the analysis is based. The name convention is CHILDNAME_Visit_SESSIONNUMBER.wav (e.g., RR_Visit_2.wav). There are 3 .wav files per each session: the full session; the audio only for the child (cut and glued together); the audio only for the parent (cut and glued together). 

## Steps

### Step 1: Set up virtual environment
```
bash setup_venv.sh
```

### Step 2: Activate virtual environment 
```
source venv/bin/activate
```

### Step 3: Extract Features
This repository contains code for three distinct types of feature extraction. 

The first is extracting acoustic features with openSMILE. This step can be replicated by running the code in the notebook `opensmile_features.ipynb`. The code was written and tested on a Macbook Pro with an M1 chip (16 GB RAM) running the macOS Sonoma 14.1 operating system. The use of a notebook environment for this task was necessitated by certain compatibility considerations between the Macbook hardware and the OpenSMILE software. The specific nature of these compatibility issues is currently under investigation. 

The second is extracting the median fundamental frequency (f0) and f0 variability (IQR) for each conversational turn based on a) the diarised corpus `data/TurnTakingData.csv` and b) the f0 extraction files in the folder `data/f0_extracted` (these files were extracted using `Praat` from the full session wav). To do this, run the following script (the outputted data will be stored in `outputs/TurnTakingData_f0.csv`):

```
python src/fundamental_freq.py
```

The third is extracting the articulation rate for each conversational turn. The articulation rate is calculated by dividing the total number of syllables with the duration of the individual utterances excluding intra-speaker pauses. The articulation rate is extracted based on a) the diarised corpus `data/TurnTakingData.csv` and b) the pauses and vowel onset files in the folder `data/textgrid`. The files in this folder are extracted using `Praat` based on the full session `wav`.  To do this, run the following script (the outputted data will be stored in `outputs/TurnTakingData_articulation.csv`):

```
python src/articulation_rate.py
```

## Project Organisation
The data was structured in the following manner, and running the code requires you to have the data organised in a corresponding folder structure. The data is not included in this repository.


```
├── data                                         Not in repository                            
│   ├── CDS_wavs 
│   ├── CDS_wavs 
│           └── childname_Visit_X.wav
│           └── ...
│       └── f0_extracted
│           └── childname_Visit_X_f0.txt         Fundamental frequency (not diarised)
│           └── ...
│       └── textgrid
│           └── childname_Visit_X.TextGrid       TextGrid files from Praat
│           └── ...
│       └── TurnTakingData.csv                   Diarised corpus
├── src 
│   └── opensmile_features.ipynb                 Notebook for extracting eGeMAPSv02 features with opensmile 
│   └── fundamental_freq.py                      Script for summarising fundamental frequency
│   └── articulation_rate.py                     Script for extracting articulation rate
├── outputs                                      Outputs from running the scripts
├── README.md
├── requirements.txt
├── setup.sh
├── get_ipykernel.sh
```
