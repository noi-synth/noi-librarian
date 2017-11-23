from librosa import load, to_mono, resample

def loadaudio(filename):
    y, sr = load(filename)
    
    # Force mono
    y = to_mono(y)
    
    # Downsample
    # y = resample(y, sr, 5512)
    
    return (y, sr)