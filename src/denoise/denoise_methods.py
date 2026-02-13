def high_pass_filter(data, cutoff_freq, sample_rate, order):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist

    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)

    y = signal.filtfilt(b, a, data)

    return y

def denoise(data, sample_rate):
    reduced_noise = noisereduce.reduce_noise(y=data, sr=sample_rate)

    return reduced_noise