import pandas as pd
import numpy as np

NUM_AMOSTRAS_SAUDAVEIS = 400
NUM_AMOSTRAS_NAO_SAUDAVEIS = 400 

# Saudáveis
temp_saudavel = np.random.normal(loc=24, scale=2, size=NUM_AMOSTRAS_SAUDAVEIS)
umid_saudavel = np.random.normal(loc=55, scale=5, size=NUM_AMOSTRAS_SAUDAVEIS)
luz_saudavel = np.random.normal(loc=2500, scale=300, size=NUM_AMOSTRAS_SAUDAVEIS)

df_saudavel = pd.DataFrame({
    'temperatura': temp_saudavel,
    'umidade': umid_saudavel,
    'luz': luz_saudavel,
    'estado': 1 # 1 = Saudável
})

# Não Saudáveis 
# Cenário A: Risco de Fungos (Frio, Úmido, Escuro)
num_cenario_a = NUM_AMOSTRAS_NAO_SAUDAVEIS // 2
temp_nao_saudavel_a = np.random.normal(loc=15, scale=2, size=num_cenario_a)
umid_nao_saudavel_a = np.random.normal(loc=85, scale=5, size=num_cenario_a)
luz_nao_saudavel_a = np.random.normal(loc=300, scale=100, size=num_cenario_a)

df_nao_saudavel_a = pd.DataFrame({
    'temperatura': temp_nao_saudavel_a,
    'umidade': umid_nao_saudavel_a,
    'luz': luz_nao_saudavel_a,
    'estado': 0 # 0 = Não Saudável
})

# Cenário B: Estresse por Calor (Quente, Seco, Luz Excessiva)
num_cenario_b = NUM_AMOSTRAS_NAO_SAUDAVEIS - num_cenario_a
temp_nao_saudavel_b = np.random.normal(loc=35, scale=3, size=num_cenario_b)
umid_nao_saudavel_b = np.random.normal(loc=30, scale=5, size=num_cenario_b)
luz_nao_saudavel_b = np.random.normal(loc=3800, scale=200, size=num_cenario_b)

df_nao_saudavel_b = pd.DataFrame({
    'temperatura': temp_nao_saudavel_b,
    'umidade': umid_nao_saudavel_b,
    'luz': luz_nao_saudavel_b,
    'estado': 0 # Rótulo 0 = Não Saudável
})

df_final = pd.concat([df_saudavel, df_nao_saudavel_a, df_nao_saudavel_b], ignore_index=True)
df_final = df_final.sample(frac=1).reset_index(drop=True)

df_final['temperatura'] = df_final['temperatura'].round(2)
df_final['umidade'] = df_final['umidade'].round(2)
df_final['luz'] = df_final['luz'].astype(int).clip(lower=0) # Garante que a luz não seja negativa

NOME_ARQUIVO = 'dataset_plantas_sintetico.csv'
df_final.to_csv(NOME_ARQUIVO, index=False)

print(f"Dataset sintético '{NOME_ARQUIVO}' gerado com sucesso!")
print(f"Total de amostras: {len(df_final)}")
print("\nExemplo dos dados gerados:")
print(df_final.head())