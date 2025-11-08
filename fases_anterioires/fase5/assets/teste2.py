# -*- coding: utf-8 -*-
"""
Predição de Yield com 5 modelos + explicações LIME e SHAP
- Modelos: LinearRegression, RidgeCV, SVR(RBF), RandomForest, GradientBoosting
- Métricas: R2, MAE, RMSE (cross-val e holdout)
- Interpretação: LIME (HTML) e SHAP (summary PNG + force plot HTML)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# === 0) Caminho do CSV (ajuste se necessário)
CSV_PATH = "crop_yield copy.csv"
OUT_DIR = "model_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# === 1) Carregar e preparar base
df = pd.read_csv(CSV_PATH)

target = "Yield"
categorical = ["Crop"]  # categóricas
numeric = [c for c in df.columns if c not in categorical + [target]]

X = df[categorical + numeric].copy()
y = df[target].copy()

# Pré-processamento:
# - OneHot para 'Crop'
# - Scale para numéricas (necessário para SVR/Linear/Ridge; inócuo para árvores)
preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
        ("num", StandardScaler(), numeric),
    ],
    remainder="drop",
)

# === 2) Definir modelos (5)
models = {
    "LinearRegression": LinearRegression(),
    "RidgeCV": RidgeCV(alphas=np.logspace(-3, 3, 25), cv=5),
    "SVR_RBF": SVR(kernel="rbf", C=10.0, epsilon=0.1, gamma="scale"),
    "RandomForest": RandomForestRegressor(
        n_estimators=400, max_depth=None, random_state=42, n_jobs=-1
    ),
    "GradientBoosting": GradientBoostingRegressor(random_state=42)
}

# Empacotar em pipelines
pipelines = {name: Pipeline([("prep", preprocess), ("model", mdl)])
             for name, mdl in models.items()}

# === 3) Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# === 4) Avaliação: K-Fold e Teste
def rmse(y_true, y_pred): return mean_squared_error(y_true, y_pred)

results = []
kf = KFold(n_splits=5, shuffle=True, random_state=42)

for name, pipe in pipelines.items():
    # Cross-val (R2, MAE, RMSE)
    r2_cv = cross_val_score(pipe, X, y, cv=kf, scoring="r2")
    mae_cv = -cross_val_score(pipe, X, y, cv=kf, scoring="neg_mean_absolute_error")
    rmse_cv = np.sqrt(-cross_val_score(pipe, X, y, cv=kf, scoring="neg_mean_squared_error"))

    # Fit + teste
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    res = {
        "model": name,
        "r2_cv_mean": r2_cv.mean(),
        "mae_cv_mean": mae_cv.mean(),
        "rmse_cv_mean": rmse_cv.mean(),
        "r2_test": r2_score(y_test, y_pred),
        "mae_test": mean_absolute_error(y_test, y_pred),
        "rmse_test": rmse(y_test, y_pred),
    }
    results.append(res)

# Tabela comparativa
df_metrics = pd.DataFrame(results).sort_values(by="rmse_test")
print("\n=== MÉTRICAS (ordenado por RMSE de teste) ===")
print(df_metrics.to_string(index=False))

# Salvar CSV de métricas
df_metrics.to_csv(os.path.join(OUT_DIR, "metrics_comparison.csv"), index=False)
print(f"\nMétricas salvas em: {os.path.abspath(os.path.join(OUT_DIR, 'metrics_comparison.csv'))}")

# === 5) Escolher 1 instância para explicação
# Pegar uma linha “típica” do conjunto de teste
idx_instance = X_test.index[0]
x_instance = X_test.loc[idx_instance:idx_instance]  # dataframe 1xD

# === 6) LIME (explicação local)
# Obs.: LIME precisa de dados já transformados? Podemos dar o predict do pipeline direto.
from lime.lime_tabular import LimeTabularExplainer

# Treinar um explainer com os dados de treino já PRE (pré-processados)
# Para isso, transformamos X_train com o preprocessador para o array numérico final e pegamos os nomes das features.
# Pegando os nomes pós-one-hot + scale
ohe = pipelines["LinearRegression"].named_steps["prep"].named_transformers_["cat"]
feat_cat_names = list(ohe.get_feature_names_out(categorical))
feat_num_names = numeric
feature_names = feat_cat_names + feat_num_names

X_train_trans = pipelines["LinearRegression"].named_steps["prep"].fit_transform(X_train)
X_test_trans  = pipelines["LinearRegression"].named_steps["prep"].transform(X_test)

lime_explainer = LimeTabularExplainer(
    training_data=np.array(X_train_trans),
    feature_names=feature_names,
    verbose=True,
    mode="regression"
)

# Função de previsão que usa o pipeline escolhido
# (vamos explicar o melhor modelo pela métrica de teste)
best_model_name = df_metrics.iloc[0]["model"]
best_pipe = pipelines[best_model_name]
best_pipe.fit(X_train, y_train)

def predict_fn(arr):
    # arr já está no espaço transformado do LIME (pós-preprocess)
    # então precisamos só da regressão final; vamos aplicar o .predict no modelo interno:
    model = best_pipe.named_steps["model"]
    return model.predict(arr)

# Gerar explicação LIME para a instância escolhida
# Precisamos transformar a mesma instância com o preprocess e passar para LIME
x_instance_trans = best_pipe.named_steps["prep"].transform(x_instance)
lime_exp = lime_explainer.explain_instance(
    data_row=x_instance_trans[0],
    predict_fn=predict_fn,
    num_features=10
)

lime_html_path = os.path.join(OUT_DIR, f"lime_{best_model_name}_instance_{idx_instance}.html")
lime_exp.save_to_file(lime_html_path)
print(f"LIME salvo em: {os.path.abspath(lime_html_path)}")

# === 7) SHAP (explicação global/local)
import shap
shap_output_dir = os.path.join(OUT_DIR, "shap")
os.makedirs(shap_output_dir, exist_ok=True)

# Preparar um "masc" (background) pequeno para métodos kernel quando necessário
background = shap.sample(pd.DataFrame(X_train_trans, columns=feature_names), 50, random_state=42)
Xtest_df = pd.DataFrame(X_test_trans, columns=feature_names)

# Escolher explicador de acordo com o tipo
final_est = best_pipe.named_steps["model"]

try:
    # Tenta TreeExplainer (funciona para RF/GBR)
    explainer = shap.TreeExplainer(final_est)
    shap_values = explainer(Xtest_df)
except Exception:
    try:
        # Tenta LinearExplainer para modelos lineares
        explainer = shap.LinearExplainer(final_est, background)
        shap_values = explainer(Xtest_df)
    except Exception:
        # Fallback: KernelExplainer (genérico; pode ser mais lento)
        explainer = shap.KernelExplainer(final_est.predict, background)
        shap_values = explainer.shap_values(Xtest_df, nsamples=200)

# Summary plot (importância média absoluta)
plt.figure()
shap.plots.beeswarm(shap_values, max_display=15, show=False)
plt.tight_layout()
summary_png = os.path.join(shap_output_dir, f"summary_{best_model_name}.png")
plt.savefig(summary_png, dpi=160, bbox_inches="tight")
plt.close()
print(f"SHAP summary PNG salvo em: {os.path.abspath(summary_png)}")
plt.show()
# Force plot para a mesma instância do LIME
try:
    force = shap.plots.force(explainer.expected_value, shap_values.values[0,:], Xtest_df.iloc[0,:], matplotlib=False)
    force_html = os.path.join(shap_output_dir, f"force_{best_model_name}_instance_{idx_instance}.html")
    shap.save_html(force_html, force)
    print(f"SHAP force plot salvo em: {os.path.abspath(force_html)}")
except Exception as e:
    print("Não foi possível gerar force plot SHAP (ok continuar):", e)

print("\nConcluído.")