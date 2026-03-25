import os
from src.config.settings import SAMPLE_RATE, DCASE2022_DEV_PATH, MACHINE_TYPE, TARGET_SECTION
from src.data.dataset import load_and_preprocess_data
from src.models.train_ocsvm import tune_ocsvm
from src.models.train_iforest import tune_iforest
from src.evaluation.metrics import evaluate_model, plot_confusion_matrices
from src.evaluation.explainability import plot_shap_summary

def main():
    # 1. Configs and Data Loading
    machine_dir = DCASE2022_DEV_PATH / MACHINE_TYPE
    feature_names = ["RMS", "Kurtosis", "Skewness", "Peak-to-Peak", "Crest_Factor", "Mean", "Std", "Entropy"] + [f"MFCC_{i}" for i in range(32)]
    
    print("\n" + "="*50)
    print("LEITURA E SEPARAÇÃO DOS DADOS")
    print("="*50)
    data = load_and_preprocess_data(machine_dir, TARGET_SECTION, SAMPLE_RATE)
    
    X_train = data['X_train_scaled']
    X_val = data['X_val_scaled']
    y_val = data['y_val']
    X_test = data['X_test_scaled']
    y_test = data['y_test']

    # 2. Grid Search
    print("\n" + "="*50)
    print("INICIANDO FINE-TUNING DE HIPERPARÂMETROS")
    print("="*50)
    
    best_ocsvm, auc_ocsvm, params_ocsvm = tune_ocsvm(X_train, X_val, y_val)
    print(f"-> Melhor OCSVM AUC-Val: {auc_ocsvm:.2%} | Params: {params_ocsvm}")
    
    best_iforest, auc_if, params_if = tune_iforest(X_train, X_val, y_val)
    print(f"-> Melhor Isolation Forest AUC-Val: {auc_if:.2%} | Params: {params_if}")

    # 3. Final Test
    print("\n" + "="*50)
    print("AVALIAÇÃO NO CONJUNTO DE TESTE FINAL (INTOCADO)")
    print("="*50)
    
    preds_ocsvm = evaluate_model(best_ocsvm, "best One-Class SVM", X_test, y_test)
    preds_iforest = evaluate_model(best_iforest, "Melhor Isolation Forest", X_test, y_test)
    
    plot_confusion_matrices(y_test, preds_ocsvm, preds_iforest)
    
    # 4. Explainability
    plot_shap_summary(best_iforest, X_test, feature_names)

if __name__ == "__main__":
    main()
