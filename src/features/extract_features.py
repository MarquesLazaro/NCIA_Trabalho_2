import librosa 
import numpy as np


def get_mel_spectrogram(signal, params):
    mel = librosa.feature.melspectrogram(y=signal, **params)

    log_mel = librosa.power_to_db(mel, ref=1.0)

    return log_mel.astype(np.float32)


def get_mfcc(signal, params):
    mfcc = librosa.feature.mfcc(y=signal, **params)

    return mfcc.astype(np.float32)
