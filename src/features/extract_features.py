def get_mel_spectrogram(signal, params):
  mel_spectrogram = librosa.feature.melspectrogram(y=signal, **params)

  log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

  return log_mel_spectrogram

def get_mfcc(log_mel_spectrogram, params):
  mfccs = librosa.feature.mfcc(S=log_mel_spectrogram, **params)

  return mfccs