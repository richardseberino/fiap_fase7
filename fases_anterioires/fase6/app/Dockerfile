# ====================================================================
# Etapa 1: Base - Escolha a Imagem PyTorch (com ou sem GPU)
# ====================================================================

# Se você planeja usar GPU (recomendado para Faster R-CNN):
# Escolha a versão que corresponda à sua versão de CUDA. 
# Exemplo: python:3.10 e cuda:11.8
FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime as base

# Se você for usar apenas CPU:
# FROM python:3.10-slim as base 

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# ====================================================================
# Etapa 2: Instalação das Dependências
# ====================================================================

# Copia apenas o arquivo de requisitos e instala as dependências.
# Isso melhora o cache do Docker.
COPY requirements.txt .

# Atualiza pip e instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# ====================================================================
# Etapa 3: Copiar a Aplicação e Configurar
# ====================================================================

# Copia os arquivos da aplicação
# Inclua seu arquivo .pth aqui
COPY app.py .
COPY templates templates/
COPY modelo1.pth .
# Certifique-se de que o nome do arquivo abaixo corresponde ao MODEL_PATH no seu app.py
# Exemplo:

# ====================================================================
# Etapa 4: Configuração de Execução
# ====================================================================

# Porta que o Flask estará executando
EXPOSE 5000

# Comando para iniciar o servidor Flask quando o contêiner for iniciado
# O host 0.0.0.0 torna o servidor acessível externamente (fora do contêiner)
CMD ["python", "app.py", "--host", "0.0.0.0"]