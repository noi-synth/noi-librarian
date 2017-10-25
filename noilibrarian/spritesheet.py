from os.path import join
from audionotebooks import ffmpeg_save_audio
import numpy as np

def create():
    data_root = 'data/drums/'
    sr = 48000 # this is the samplerate initially used to load the samples
    total_limit = 100 #None # set this to 100 to export 100 samples
    length_limit = sr/8 # set this to sr/4 to only export 250ms of audio per sample
    %time samples = np.load(join(data_root, 'samples.npy'))
    y = samples[:total_limit, :length_limit].reshape(-1)
    %time ffmpeg_save_audio(data_root + 'spritesheet.mp3', y, sr)