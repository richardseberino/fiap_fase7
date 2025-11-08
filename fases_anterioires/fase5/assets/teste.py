# -*- coding: utf-8 -*-
"""
Clustering não supervisionado para a base de culturas
- Explora Hierárquico (dendrograma)
- Define k candidato com Silhouette (varrendo k)
- Ajusta K-Means e Agglomerative
- Compara clusters x 'Crop'
- Gera gráficos: dendrograma, elbow, PCA 2D
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

from scipy.cluster.hierarchy import linkage, dendrogram

# ----------------------------
# 1) Carregar os dados
# ----------------------------
# Ajuste o caminho do CSV conforme necessário
CSV_PATH = "crop_yield copy.csv"  # substitua se necessário

df = pd.read_csv(CSV_PATH)

# ----------------------------
# 2) Configurações do experimento
# ----------------------------
target_col_for_eval = "Crop"  # usado apenas para avaliação/comparação
include_yield = True          # se True, inclui "Yield" entre as features do clustering
random_state = 42

# Selecionar colunas numéricas
num_cols = df.select_dtypes(include=["number", "float64", "int64"]).columns.tolist()

# Se não quiser usar Yield no clustering, remova
if not include_yield and "Yield" in num_cols:
    num_cols.remove("Yield")

# Remover a coluna categórica 'Crop' das features (se estiver codificada como número em algum contexto)
if target_col_for_eval in num_cols:
    num_cols.remove(target_col_for_eval)

X = df[num_cols].copy()

# ----------------------------
# 3) Padronização
# ----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------------
# 4) Dendrograma (Hierárquico) para exploração
# ----------------------------
plt.figure(figsize=(10, 5))
Z = linkage(X_scaled, method="ward")
dendrogram(Z, truncate_mode="lastp", p=20, leaf_rotation=45., leaf_font_size=10.)
plt.title("Dendrograma (Hierárquico - método Ward)")
plt.xlabel("Grupos (truncado)")
plt.ylabel("Distância")
plt.tight_layout()
plt.show()

# ----------------------------
# 5) Escolha do k (número de clusters)
#    - Curva do cotovelo (inertia) para K-Means
#    - Silhouette para k = 2..8
# ----------------------------
k_range = range(2, 9)

inertias = []
silhouettes = []

for k in k_range:
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    labels_km = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil = silhouette_score(X_scaled, labels_km)
    silhouettes.append(sil)

best_k = k_range[int(np.argmax(silhouettes))]

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Elbow
ax[0].plot(list(k_range), inertias, marker="o")
ax[0].set_title("K-Means - Curva do Cotovelo (Inertia)")
ax[0].set_xlabel("k")
ax[0].set_ylabel("Inertia")
ax[0].grid(True)

# Silhouette
ax[1].plot(list(k_range), silhouettes, marker="o")
ax[1].set_title("K-Means - Silhouette por k")
ax[1].set_xlabel("k")
ax[1].set_ylabel("Silhouette")
ax[1].axvline(best_k, linestyle="--", alpha=0.6)
ax[1].grid(True)

plt.tight_layout()
plt.show()

print(f"Melhor k por Silhouette (K-Means): {best_k:.0f} | Silhouette = {max(silhouettes):.4f}")

# ----------------------------
# 6) Ajustar K-Means e Agglomerative com best_k
# ----------------------------
kmeans = KMeans(n_clusters=best_k, random_state=random_state, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)
sil_kmeans = silhouette_score(X_scaled, labels_kmeans)

agglo = AgglomerativeClustering(n_clusters=best_k, linkage="ward")
labels_agglo = agglo.fit_predict(X_scaled)
sil_agglo = silhouette_score(X_scaled, labels_agglo)

print(f"Silhouette (K-Means, k={best_k}): {sil_kmeans:.4f}")
print(f"Silhouette (Agglomerative, k={best_k}): {sil_agglo:.4f}")

# Anexar rótulos ao DataFrame
df["cluster_kmeans"] = labels_kmeans
df["cluster_agglo"] = labels_agglo

# ----------------------------
# 7) Comparar clusters com a coluna 'Crop' (apenas avaliação)
# ----------------------------
if target_col_for_eval in df.columns:
    print("\nContingência Crop x cluster_kmeans:")
    print(pd.crosstab(df[target_col_for_eval], df["cluster_kmeans"]))

    print("\nContingência Crop x cluster_agglo:")
    print(pd.crosstab(df[target_col_for_eval], df["cluster_agglo"]))

# ----------------------------
# 8) Visualização em 2D via PCA
# ----------------------------
pca = PCA(n_components=2, random_state=random_state)
X_pca = pca.fit_transform(X_scaled)

df_plot = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
df_plot["cluster_kmeans"] = labels_kmeans
df_plot["cluster_agglo"] = labels_agglo
if target_col_for_eval in df.columns:
    df_plot[target_col_for_eval] = df[target_col_for_eval].values

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.scatterplot(data=df_plot, x="PC1", y="PC2", hue="cluster_kmeans", palette="Set1", ax=ax[0])
ax[0].set_title(f"PCA 2D - K-Means (k={best_k})")

sns.scatterplot(data=df_plot, x="PC1", y="PC2", hue="cluster_agglo", palette="Set2", ax=ax[1])
ax[1].set_title(f"PCA 2D - Agglomerative (k={best_k})")

plt.tight_layout()
plt.show()

# ----------------------------
# 9) (Opcional) Salvar resultados
# ----------------------------
OUT_CSV = "clustered_output.csv"
df.to_csv(OUT_CSV, index=False)
print(f"\nArquivo com clusters salvo em: {os.path.abspath(OUT_CSV)}")

# ----------------------------
# 10) Resumo
# ----------------------------
print("\nResumo:")
print(f"- Features usadas no clustering: {num_cols}")
print(f"- include_yield = {include_yield}")
print(f"- Melhor k (por Silhouette/K-Means): {best_k}")
print(f"- Silhouette K-Means: {sil_kmeans:.4f}")
print(f"- Silhouette Agglomerative: {sil_agglo:.4f}")