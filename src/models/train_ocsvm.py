from sklearn.svm import OneClassSVM
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import ParameterGrid
from tqdm import tqdm

def tune_ocsvm(X_train, X_val, y_val):
    param_grid_ocsvm = {
        'nu': [0.001, 0.01, 0.05, 0.1, 0.2],
        'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 0.5],
        'kernel': ['rbf', 'poly', 'sigmoid']
    }

    best_auc_ocsvm = 0
    best_ocsvm = None
    best_params_ocsvm = {}

    grid_ocsvm = list(ParameterGrid(param_grid_ocsvm))
    print(f"Testando {len(grid_ocsvm)} combinações para o One-Class SVM...")

    for params in tqdm(grid_ocsvm, desc="OCSVM Grid"):
        ocsvm = OneClassSVM(**params)
        ocsvm.fit(X_train)
        scores_val = -ocsvm.decision_function(X_val)
        auc_val = roc_auc_score(y_val, scores_val)
        
        if auc_val > best_auc_ocsvm:
            best_auc_ocsvm = auc_val
            best_ocsvm = ocsvm
            best_params_ocsvm = params

    return best_ocsvm, best_auc_ocsvm, best_params_ocsvm
