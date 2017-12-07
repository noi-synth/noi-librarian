from noilibrarian.audio import loadaudio
from librosa import feature, display, dtw, resample, stft
import numpy as np
import noilibrarian.library

def loadreference(refname):
    return loadaudio('noilibrarian/reference/' + refname + '.wav')

def getscore(wp):
    distance = 0
    for row in wp:
        distance += abs(row[0] - row[1])
    return distance
        

def compareto(audio, reference):
    xy, xsr = audio
    yy, ysr = reference
    
    mfccX = feature.mfcc(y=xy, sr=xsr)
    mfccY = feature.mfcc(y=yy, sr=ysr) 
    
    chromaX = feature.chroma_cqt(y=xy, sr=xsr)
    chromaY = feature.chroma_cqt(y=yy, sr=ysr) 
    
    distances = []
    score = 0
    
    D, wp = dtw(mfccX[0], mfccY[0])
    score += getscore(wp) * 2
    
    D, wp = dtw(chromaX, chromaY)
    score += getscore(wp)
    
    distances.append(score / 3)
    
    return sum(distances) / len(distances)

def classify(audio):    
    distances = [
        { 'category': 'kick', 'distance': compareto(audio, loadreference('kick')) },
        { 'category': 'snare', 'distance': compareto(audio, loadreference('snare')) },
        { 'category': 'hihat', 'distance': compareto(audio, loadreference('hihat')) },
    ]
    
    distances.sort(key=lambda x: x['distance'])
    
    print(distances)
    
    return (distances[0]['category'], distances[0]['distance'], distances[1]['category'])