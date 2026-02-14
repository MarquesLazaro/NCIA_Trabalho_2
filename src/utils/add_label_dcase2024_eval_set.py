from pathlib import Path

import pandas as pd


def add_label_dcase2024_eval_set(dcase2024_eval_path):
    LABELS_ROOT_PATH = "data/ground_truth_data"

    for machine_dir in Path(dcase2024_eval_path).iterdir():
        data_dir = machine_dir / "test"
        labels_path = (
            LABELS_ROOT_PATH + f"/ground_truth_{machine_dir.name}_section_00_test.csv"
        )
    labels_df = pd.read_csv(labels_path, names=["filename", "label"], header=None)
    labels_df.set_index("filename", inplace=True)

    for sound_file in data_dir.iterdir():
        if sound_file.name in labels_df.index:
            label = labels_df.loc[sound_file.name, "label"]
            label_name = "normal" if label == 0 else "anomaly"
            new_name = (
                f'{sound_file.name.removesuffix('.wav')}_source_eval_{label_name}.wav'
            )

            sound_file.rename(sound_file.with_name(new_name))
