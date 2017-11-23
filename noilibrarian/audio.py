from librosa import load, to_mono

def loadaudio(filename):
    y, sr = load(filename)
    
    return (to_mono(y), sr)