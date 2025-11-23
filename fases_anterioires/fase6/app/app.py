import torch
import torchvision
import torchvision.transforms as T
import numpy as np
from PIL import Image, ImageDraw
import io
import base64
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify

# --- Configurações ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# Definir o dispositivo (GPU se disponível, senão CPU)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Lista de nomes de classes do COCO para mapear os IDs de labels do modelo
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'lagarta', "percevejo marrom"
]


MODEL_PATH = 'modelo1.pth' 
# IMPORTANTE: Mude 91 para o número de classes com o qual você treinou seu modelo (+1 para o background)
N_CLASSES = 3

# ... (N_CLASSES e MODEL_PATH definidos)

# --- Carregamento do Modelo ---
@app.before_request
def load_model():
    """Carrega o seu modelo Faster R-CNN treinado."""
    if not hasattr(app, 'model'):
        print(f"Carregando o modelo Faster R-CNN no dispositivo: {DEVICE}...")
        
        # 1. Cria a arquitetura do modelo
        app.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights=None, 
            num_classes=N_CLASSES
        )
        
        # 2. Carrega o OBJETO COMPLETO do seu arquivo .pth
        try:
            print("Tentando carregar o modelo como objeto completo...")
            
            # Carrega o objeto completo do modelo (inclui a arquitetura e os pesos)
            loaded_object = torch.load(
                MODEL_PATH, 
                map_location=DEVICE,
                weights_only=False # Necessário para carregar o objeto completo
            )

            # Verifica se o objeto carregado é o modelo
            if isinstance(loaded_object, torch.nn.Module):
                # Se for o modelo completo, você pode carregá-lo diretamente OU
                # (Recomendado) Obter o dicionário de estado dele:
                state_dict = loaded_object.state_dict()
            else:
                # Se for o state_dict, ele já será um dict e o código continuará.
                state_dict = loaded_object
            
            # Aplica os pesos à arquitetura do modelo que inicializamos no passo 1.
            # Este passo é necessário para garantir que o modelo esteja dentro do Flask.
            app.model.load_state_dict(state_dict) 
            
            print(f"Pesos carregados de {MODEL_PATH} com sucesso.")
            
        except FileNotFoundError:
            print(f"ERRO: Arquivo de modelo não encontrado em {MODEL_PATH}.")
            
        # 3. Coloca o modelo em modo de avaliação
        app.model.eval()
        app.model.to(DEVICE)
        print("Modelo carregado e pronto para inferência.")

# --- Funções de Detecção e Visualização ---
def detect_and_draw(image_data):
    """
    Executa a detecção de objetos na imagem e desenha os bounding boxes.
    Retorna a imagem processada em formato base64 e os resultados textuais.
    """
    # 1. Pré-processamento da imagem
    transform = T.Compose([T.ToTensor()])
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    img_tensor = transform(img).to(DEVICE)
    
    # 2. Inferência (detecção)
    with torch.no_grad():
        # O modelo espera uma lista de tensores de imagem
        prediction = app.model([img_tensor]) 

    # 3. Pós-processamento e Desenho
    results = prediction[0]
    draw = ImageDraw.Draw(img)
    detections = []
    
    # Define um limiar de confiança (score) para exibir as detecções
    score_threshold = 0.7 

    for box, label, score in zip(results['boxes'], results['labels'], results['scores']):
        if score.item() > score_threshold:
            # Converte as coordenadas do tensor para a imagem PIL
            box = box.cpu().numpy().astype(int)
            x1, y1, x2, y2 = box
            
            label_name = COCO_INSTANCE_CATEGORY_NAMES[label.item()]
            
            # Desenha o Bounding Box
            draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
            
            # Desenha o texto (classe e score)
            text = f"{label_name}: {score.item():.2f}"
            
            # Posição do texto (acima do box)
            text_x, text_y = x1, y1 - 10 
            if text_y < 0: # Ajusta se sair do limite superior
                text_y = y2 + 5 

            draw.text((text_x, text_y), text, fill="red")
            
            detections.append(f"{label_name} com confiança de {score.item():.2f}")

    # 4. Converte a imagem resultante para base64 para exibição no HTML
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return img_base64, detections

# --- Rotas do Flask ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Rota principal para upload e exibição do resultado."""
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        # Verifica se o nome do arquivo está vazio
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Lê o conteúdo do arquivo
            image_data = file.read()
            
            # Executa a detecção
            processed_image_base64, detections = detect_and_draw(image_data)
            
            return render_template('index.html', 
                                   processed_image=processed_image_base64, 
                                   detections=detections)
            
    return render_template('index.html', processed_image=None, detections=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Rota da API para fazer a predição e retornar JSON."""
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    if file:
        try:
            image_data = file.read()
            processed_image_base64, detections = detect_and_draw(image_data)
            
            return jsonify({
                "image": processed_image_base64,
                "detections": detections
            })
        except Exception as e:
            return jsonify({"error": f"Erro ao processar a imagem: {str(e)}"}), 500
            
    return jsonify({"error": "Arquivo inválido"}), 400

# --- Execução ---
if __name__ == '__main__':
    # Cria a pasta de uploads se não existir (apenas por segurança, não é usada para salvar arquivos aqui)
    import os
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    app.run(host='0.0.0.0', port=5000, debug=True)