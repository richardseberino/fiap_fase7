# Gerador de Dataset Sintético para Saúde de Plantas

Este diretório contém um script Python (`gerar_dataset_ficticio.py`) projetado para criar um dataset sintético. O objetivo deste dataset é simular dados ambientais (temperatura, umidade e luz) para treinar um modelo de machine learning capaz de classificar o estado de saúde de uma planta.

## Objetivo do Script

O script gera um arquivo no formato `.csv` contendo amostras de dados que representam duas classes principais:

- **Saudável (1):** Condições ambientais ideais para o crescimento da planta.
- **Não Saudável (0):** Condições ambientais adversas que podem levar a problemas como estresse por calor ou proliferação de fungos.

## Processo de Geração do Dataset

O processo de criação dos dados é baseado na geração de números aleatórios a partir de uma distribuição normal, permitindo simular variações realistas em torno de médias pré-definidas para cada cenário.

### 1. Definição dos Parâmetros

No início do script, as constantes `NUM_AMOSTRAS_SAUDAVEIS` e `NUM_AMOSTRAS_NAO_SAUDAVEIS` definem o número de registros para cada classe, garantindo um dataset balanceado.

### 2. Geração de Dados "Saudáveis"

- As amostras saudáveis são geradas com base em parâmetros que representam um ambiente ideal:
  - **Temperatura:** Média de 24°C.
  - **Umidade:** Média de 55%.
  - **Luminosidade:** Média de 2500 lux.
- Todas as amostras desta categoria recebem o rótulo `estado = 1`.

### 3. Geração de Dados "Não Saudáveis"

Para tornar o modelo mais robusto, os dados não saudáveis são divididos em dois cenários distintos:

#### Cenário A: Risco de Fungos (Frio, Úmido, Escuro)
- Simula condições propícias para o desenvolvimento de doenças fúngicas.
  - **Temperatura:** Média de 15°C.
  - **Umidade:** Média de 85%.
  - **Luminosidade:** Média de 300 lux.

#### Cenário B: Estresse por Calor (Quente, Seco, Luz Excessiva)
- Simula condições de estresse hídrico e térmico.
  - **Temperatura:** Média de 35°C.
  - **Umidade:** Média de 30%.
  - **Luminosidade:** Média de 3800 lux.

- Todas as amostras de ambos os cenários não saudáveis recebem o rótulo `estado = 0`.

### 4. Consolidação e Finalização

1.  **Concatenação:** Os DataFrames (saudável, não saudável A, não saudável B) são unidos em um único DataFrame.
2.  **Embaralhamento:** As linhas do dataset final são embaralhadas (`.sample(frac=1)`) para garantir que os dados não estejam ordenados por classe, o que é crucial para o treinamento do modelo.
3.  **Limpeza:** Os valores de `temperatura` e `umidade` são arredondados para duas casas decimais, e a `luz` é convertida para inteiro, garantindo que não haja valores negativos.
4.  **Exportação:** O DataFrame final é salvo no arquivo `dataset_plantas_sintetico.csv`.

## Estrutura do Arquivo CSV

O arquivo `dataset_plantas_sintetico.csv` gerado possui as seguintes colunas:

| Coluna      | Tipo    | Descrição                                         |
|-------------|---------|---------------------------------------------------|
| `temperatura` | `float` | Temperatura do ambiente em graus Celsius (°C).    |
| `umidade`     | `float` | Umidade relativa do ar em porcentagem (%).        |
| `luz`         | `int`   | Intensidade luminosa em lux.                      |
| `estado`      | `int`   | Rótulo da classe: `1` para Saudável, `0` para Não Saudável. |

## Como Usar

1.  Certifique-se de ter as bibliotecas `pandas` e `numpy` instaladas.
2.  Navegue até o diretório `/dataset` pelo terminal.
3.  Execute o script com o comando:
    ```bash
    python gerar_dataset_ficticio.py
    ```
4.  Ao final da execução, o arquivo `dataset_plantas_sintetico.csv` será criado no mesmo diretório.

Para saber mais sobre o processo de treinamento do modelo [clique aqui](../modelo/modelo_gridsearch.ipynb)