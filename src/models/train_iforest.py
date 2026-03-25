from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import ParameterGrid
from tqdm import tqdm

def tune_iforest(X_train, X_val, y_val):
    param_grid_if = {
        'n_estimators': [100, 300, 500, 1000, 10000],
        'max_samples': ['auto', 0.5, 0.8],
        'contamination': ['auto', 0.01, 0.05, 0.1, 0.15, 0.2],
        'max_features': [0.5, 0.8, 1.0]
    }

    best_auc_if = 0
    best_iforest = None
    best_params_if = {}

    grid_if = list(ParameterGrid(param_grid_if))
    print(f"\nTestando {len(grid_if)} combinações para o Isolation Forest...")

    for params in tqdm(grid_if, desc="iForest Grid"):
        iforest = IsolationForest(**params, random_state=42)
        iforest.fit(X_train)
        scores_val = -iforest.decision_function(X_val)
        auc_val = roc_auc_score(y_val, scores_val)
        
        if auc_val > best_auc_if:
            best_auc_if = auc_val
            best_iforest = iforest
            best_params_if = params

    return best_iforest, best_auc_if, best_params_if
