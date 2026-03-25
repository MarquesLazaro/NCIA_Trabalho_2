def min_max_scaler(spec):
    min_val = spec.min()
    max_val = spec.max()

    if max_val - min_val > 0:
        spec_norm = (spec - min_val) / (max_val - min_val)
    else:
        spec_norm = spec - min_val

    return spec_norm
