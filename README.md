# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Fase Final 7

## Grupo DRELL

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/douglas-souza-felipe-b815281a2/">Douglas</a>
- <a href="https://www.linkedin.com/in/richard-marques-26b3a14/">Richard</a>
- <a href="https://www.linkedin.com/in/lucasmedeirosleite">Lucas Medeiros</a> 
- <a href="https://www.linkedin.com/in/mariana-cavalcante-oliveira-987684223/">Mariana Cavalcante Oliveira</a>
- <a href="https://www.linkedin.com/in/luis-fernando-dos-santos-costa-b69894365/">Luis</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://github.com/leoruiz197">Leo Ruiz</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">Andre Godoi</a>


## 📜 Descrição

Este é o repositório final onde consolidamos todas as entregas feitas durante o ano. 

Fase 1: Modelagem de base de dados e algorítimo 

Fase 2-4: implementação da base e integração com solução IoT que captura os dados e grava nesta base de dados

Fase 5: Uso da computação em núvem para executar os projetos na AWS

Fase 6: Reconhecimento de objetos em Imagem usando YOLO
[Fase 6](fases_anterioires/fase6/README.md)


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>db</b>: Arquivos de banco de dados em geral como `schema.sql` e `seeds.py`.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## Pré requisitos para rodar localmente:
* Docker instalado
* MySQL 8 container rodando (atualize o arquivo `config/database.yml` e substitua a configuração `container` com o nome do seu container)

## 🔧 Como executar o código

*Acrescentar as informações necessárias sobre pré-requisitos (IDEs, serviços, bibliotecas etc.) e instalação básica do projeto, descrevendo eventuais versões utilizadas. Colocar um passo a passo de como o leitor pode baixar o seu código e executá-lo a partir de sua máquina ou seu repositório. Considere a explicação organizada em fase.*

### 1.0 Banco de dados

#### 1.1 Carregando o conatainer com o MySQL
Execute o comando abaixo para criar uma instancia de Banco de dados mySQL
```
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=agro_dev -e MYSQL_USER=agro -e MYSQL_PASSWORD=agro1 -p 3306:3306 -v mysql_data:/var/lib/mysql docker.io/mysql:8.0
```
Este comando vai criar uma pasta mysql_data no diretório onde você estiver rodando o comando, pois caso precise parar e subir o ambiente os dados não se percam

### 1.2 - Crie a estrutura das tabelas 
Execute o comando abaixo para carregar o script SQL que cria a estrtura das tabelas e faZ a carga inicial de dados
```
cmd /c "docker exec -i mysql mysql -u root -proot agro_dev < db/schema.sql"
```
#### 1.3 Popula o banco com dados de exemplo
* Execute o comando abaixo para carregar os dados na base MySQL
```
python .\db\seeds.py
```

### 2.0 API de Reconhecimento de imagens

#### 2.1 Carregando o container com a API da aplicação 
* Execute o comando abaixo:
```
docker run -tid -p 5000:5000 seberino/faster-cnn:1.1 
```

### 3.0 Interface Principal
Para carregar a interface princpal da aplicação, baseada em Streamlit, precisamos do Python 3.9 ou superior

#### 3.1 Crie um ambiente novo
* Execute o comando abaixo para criar um ambiente novo e ativar ele
```
python -m venv .venv
.\.venv\Scriptsactivate 
```

#### 3.2 Instale as dependencias
* Execute o comando abaixo para instalar as dependencias do projeto
```
python -m pip install -r requirements.txt
``` 

#### 3.3 Execute a aplicação
* Execute o comando abaixo para executar a aplicação principal, este comando já deve abrir seu navegador com a página padrão da aplicação
```
python -m streamlit run .\src\ui\app.py
```

## 🗃 Histórico de lançamentos

* 0.1.0 - 08/11/2025
    * Versão inicial

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


