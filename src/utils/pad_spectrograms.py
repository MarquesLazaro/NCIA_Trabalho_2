import numpy as np


def pad_spectrograms(signals):
    widths = [spec.shape[1] for spec in signals]
    target_width = max(widths)

    print(f"\nPadronizando larguras para: {target_width}")

    X_fixed = []
    for spec in signals:
        current_width = spec.shape[1]
        if current_width < target_width:
            # Preenche com zeros o que falta
            padding = ((0, 0), (0, target_width - current_width))
            spec_fixed = np.pad(spec, padding, mode="constant")
        elif current_width > target_width:
            # Corta o excesso
            spec_fixed = spec[:, :target_width]
        else:
            spec_fixed = spec
        X_fixed.append(spec_fixed)

    return X_fixed
