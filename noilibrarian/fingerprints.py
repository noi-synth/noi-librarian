from utils import *
from tqdm import *
from os.path import join
from matplotlib import pyplot as plt
from skimage.measure import block_reduce
from multiprocessing import Pool
import numpy as np
import librosa

def job(y):
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, window=window)
    amp = np.abs(S)
    if reduce_rows > 1 or reduce_cols > 1:
        amp = block_reduce(amp, (reduce_rows, reduce_cols), func=np.mean)
    if amp.shape[1] < crop_cols:
        amp = np.pad(amp, ((0, 0), (0, crop_cols-amp.shape[1])), 'constant')
    amp = amp[:crop_rows, :crop_cols]
    if use_logamp:
        amp = librosa.logamplitude(amp**2)
    amp -= amp.min()
    if amp.max() > 0:
        amp /= amp.max()
    amp = np.flipud(amp) # for visualization, put low frequencies on bottom
    return amp

def generate():
    data_root = 'data/drums/'
    n_fft = 1024
    hop_length = n_fft/4
    use_logamp = False # boost the brightness of quiet sounds
    reduce_rows = 10 # how many frequency bands to average into one
    reduce_cols = 1 # how many time steps to average into one
    crop_rows = 32 # limit how many frequency bands to use
    crop_cols = 32 # limit how many time steps to use
    limit = None # set this to 100 to only process 100 samples

    %time samples = np.load(join(data_root, 'samples.npy'))

    window = np.hanning(n_fft)

    pool = Pool()
    %time fingerprints = pool.map(job, samples[:limit])
    fingerprints = np.asarray(fingerprints).astype(np.float32)

    np.save(join(data_root, 'fingerprints.npy'), fingerprints)

    print 'data shape:', np.shape(fingerprints)

    mean = np.mean(fingerprints, axis=0)
    mean -= mean.min()
    mean /= mean.max()

    print 'mean:'
    show_array(255 * mean)
    print 'max:'
    show_array(255 * np.max(fingerprints, axis=0))

    print 'random selection:'
    indices = range(len(fingerprints))
    np.random.shuffle(indices)
    show_array(255 * make_mosaic(np.array(fingerprints)[indices], n=16))