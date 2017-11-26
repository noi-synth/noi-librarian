from noilibrarian.audio import loadaudio
from librosa import feature, display, dtw, resample
import numpy as np
import matplotlib.pyplot as plt

def loadreference(refname):
    return loadaudio('noilibrarian/reference/' + refname + '.wav')

def compareto(audio, reference):
    xy, xsr = audio
    yy, ysr = reference
    
    X = feature.chroma_stft(y=xy, sr=xsr)
    Y = feature.chroma_stft(y=yy, sr=ysr)
    
    mfccD, mfccWP = dtw(X, Y, subseq=True)
    wfD, wfWP = dtw(resample(xy, xsr, 64), resample(yy, ysr, 64), subseq=True)

    distance = 0

    for row in mfccWP:
        distance += abs(row[0] - row[1])
        
    for row in wfWP:
         distance += abs(row[0] - row[1])
        
    return distance / (len(mfccWP) + len(wfWP))

def classify(audio):    
    distances = {
        'kick': compareto(audio, loadreference('kick')),
        'snare': compareto(audio, loadreference('snare')),
        'hihat': compareto(audio, loadreference('hihat')),
    }
    
    lowest = ('none', float('inf'))
    
    for distance in distances:
        if distances[distance] < lowest[1]:
            lowest = (distance, distances[distance])
        
    print(' \_ lowest distance is {}', lowest)
    
    return lowest