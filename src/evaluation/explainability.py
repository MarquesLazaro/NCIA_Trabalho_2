import shap
import matplotlib.pyplot as plt

def plot_shap_summary(model, X_test, feature_names):
    print("\n--- Gerando Explicabilidade (SHAP) ---")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    plt.figure(figsize=(10, 6))
    plt.title("Impacto das Features (SHAP Summary Plot)")
    sv = shap_values[1] if isinstance(shap_values, list) else shap_values
    shap.summary_plot(sv, X_test, feature_names=feature_names)
    plt.show()
