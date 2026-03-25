import numpy as np
import librosa
import scipy.stats
from scipy.signal import butter, sosfilt

def highpass_filter(signal, sr=16000, cutoff=80, order=4):
    nyq = 0.5 * sr
    cutoff_n = cutoff / nyq
    sos = butter(order, cutoff_n, btype="highpass", output="sos")
    return sosfilt(sos, signal).astype(np.float32)

def peak_normalize(signal):
    peak = np.max(np.abs(signal))
    if peak > 0:
        return signal / peak
    return signal

def extract_dcase_features(file_path, sample_rate=16000):
    signal, sr = librosa.load(file_path, sr=sample_rate, mono=True)
    
    rms = np.sqrt(np.mean(signal**2))
    kurt = scipy.stats.kurtosis(signal)
    skew = scipy.stats.skew(signal)
    p2p = np.ptp(signal) 
    crest = np.max(np.abs(signal)) / (rms + 1e-8) 
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    
    hist, _ = np.histogram(signal, bins=256, density=True)
    hist = hist[hist > 0]
    entropy = scipy.stats.entropy(hist)

    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=32)
    mel_spec = librosa.feature.melspectrogram(y=signal, sr=sr, n_mels=32)
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)
   
    mfccs_mean = np.mean(mfccs, axis=1)
    basic_features = np.array([rms, kurt, skew, p2p, crest, mean_val, std_val, entropy]) 
    
    return np.concatenate([basic_features, mfccs_mean])
