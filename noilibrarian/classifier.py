from noilibrarian.audio import loadaudio
from librosa import feature, display, dtw, resample
import numpy as np
import matplotlib.pyplot as plt

def loadreference(refname):
    return loadaudio('noilibrarian/reference/' + refname + '.wav')

def compareto(audio, reference):
    xy, xsr = audio
    yy, ysr = reference
    
    plt.figure(figsize=(21,6))
    plt.subplot(2,4,1)
    plt.title('audio: kick3')
    display.waveplot(xy)
    plt.subplot(2,4,5)
    plt.title('reference: kick')
    display.waveplot(yy)
    
    X = feature.chroma_stft(y=xy, sr=xsr)
    Y = feature.chroma_stft(y=yy, sr=ysr)
    
    # plt.subplot(2, 4, 2)
    # display.specshow(D, x_axis='frames', y_axis='frames')
    # plt.title('DE chroma stft')
    # plt.plot(wp[:, 1], wp[:, 0], label='Optimal path', color='y')
    # plt.legend()
    # plt.subplot(2, 4, 6)
    # plt.plot(D[-1, :] / wp.shape[0])
    # # plt.xlim([0, Y.shape[1]])
    # # plt.ylim([0, 2])
    # plt.title('Matching cost function')
    # 
    # X = feature.mfcc(y=xy, sr=xsr)
    # Y = feature.mfcc(y=yy, sr=ysr)
    
    mfccD, mfccWP = dtw(X, Y, subseq=True)
    
    wfD, wfWP = dtw(resample(xy, xsr, 64), resample(yy, ysr, 64), subseq=True)

    distance = 0

    for row in mfccWP:
        distance += abs(row[0] - row[1])
        
    # for row in wfWP:
    #      distance += abs(row[0] - row[1])
        
    distance = distance / len(wfWP)
    
    print('distance: {}'.format(distance))

def classify(audio):    
    compareto(audio, loadreference('snare'))
    
    return ('snare', -99999)