import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix

def evaluate_model(model, model_name, X_test, y_test):
    scores_test = -model.decision_function(X_test)
    preds_test = [1 if x == -1 else 0 for x in model.predict(X_test)]
    auc_test = roc_auc_score(y_test, scores_test)

    print(f"\n[ RESULTADOS: {model_name} ]")
    print(f"ROC-AUC Teste: {auc_test:.2%}")
    print("Relatório de Classificação:")
    print(classification_report(y_test, preds_test, target_names=['Normal (0)', 'Anomalia (1)'], zero_division=0))
    
    return preds_test

def plot_confusion_matrices(y_test, preds_ocsvm, preds_iforest):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    cm_ocsvm = confusion_matrix(y_test, preds_ocsvm)
    sns.heatmap(cm_ocsvm, annot=True, fmt='d', cmap='Blues', ax=axes[0], xticklabels=['Normal', 'Anomalia'], yticklabels=['Normal', 'Anomalia'])
    axes[0].set_title('Matriz de Confusão OCSVM')

    cm_if = confusion_matrix(y_test, preds_iforest)
    sns.heatmap(cm_if, annot=True, fmt='d', cmap='Oranges', ax=axes[1], xticklabels=['Normal', 'Anomalia'], yticklabels=['Normal', 'Anomalia'])
    axes[1].set_title('Matriz de Confusão Isolation Forest')

    plt.tight_layout()
    plt.show()
