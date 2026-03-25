import numpy as np


def pad_audio(signal, target_len=10 * 24_000):
    """
    Padroniza o áudio para um tamanho fixo (em amostras).
    Ex: para 10s em 24kHz, target_len = 240000.
    """
    current_len = len(signal)

    if current_len < target_len:
        # Preenche com zeros no final
        padding = target_len - current_len
        signal_fixed = np.pad(signal, (0, padding), mode="constant")
    elif current_len > target_len:
        # Corta o excesso
        signal_fixed = signal[:target_len]
    else:
        signal_fixed = signal

    return signal_fixed
