from librosa import load, to_mono, resample

def loadaudio(filename):
    y, sr = load(filename)
    
    # Force mono
    y = to_mono(y)
    
    # Downsample
    # y = resample(y, sr, 5512)
    
    return (y, sr)

def loadtrimmedaudio(filename):
    y, sr = loadaudio(filename)
    
    ty = list(map(lambda x: 0 if x < 0 else x, y))
    maximum = max(ty)
    start = 0
    
    for i in range(0, len(ty)):
        if ty[i] > maximum * 0.05:
            start = i
            break
    
    return (ty[start::], sr)