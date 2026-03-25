import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.features.dcase_features import extract_dcase_features

def load_and_preprocess_data(machine_dir, target_section, sample_rate=16000):
    print(f"Lendo dados da máquina - Seção '{target_section}'...")

    X_train_raw, y_train_raw = [], []
    X_test_all, y_test_all = [], []
    
    for f in tqdm(list((machine_dir / 'train').rglob('*.wav')), desc="Extraindo Treino"):
        if target_section in f.name:
            X_train_raw.append(extract_dcase_features(f, sample_rate=sample_rate))
            y_train_raw.append(0)

    for f in tqdm(list((machine_dir / 'test').rglob('*.wav')), desc="Extraindo Avaliação"):
        if target_section in f.name:
            X_test_all.append(extract_dcase_features(f, sample_rate=sample_rate))
            label = 1 if 'anomaly' in f.name else 0
            y_test_all.append(label)

    X_train_raw = np.array(X_train_raw)
    y_train_raw = np.array(y_train_raw)

    X_val_raw, X_test_raw, y_val, y_test = train_test_split(
        X_test_all, y_test_all, test_size=0.7, random_state=42, stratify=y_test_all
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_val_scaled = scaler.transform(X_val_raw)
    X_test_scaled = scaler.transform(X_test_raw)
    
    return {
        'X_train_scaled': X_train_scaled,
        'y_train': y_train_raw,
        'X_val_scaled': X_val_scaled,
        'y_val': y_val,
        'X_test_scaled': X_test_scaled,
        'y_test': y_test,
        'scaler': scaler
    }
