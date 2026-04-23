# Aula 02 — e03 Dados Sintéticos, Serialização e Serving de Modelo

Este projeto foi desenvolvido como parte da segunda aula prática da disciplina, com foco em um fluxo simplificado de **MLOps**: geração de dados sintéticos, treinamento de modelo, serialização do artefato, publicação no Hugging Face Hub e consumo do modelo por meio de uma API FastAPI.

## Visão geral

A proposta desta aula foi simular um cenário de **detecção de fraude em transações** sem depender de dados reais. Para isso, o projeto foi dividido em etapas que representam um pipeline completo:

1. geração de dados sintéticos com variáveis de domínio  
2. treinamento de um modelo de classificação  
3. salvamento do modelo em arquivo `.pkl`  
4. publicação do artefato no Hugging Face Hub  
5. carregamento remoto do modelo  
6. exposição de predição via API

## Analogia para entender o projeto

Uma boa forma de visualizar este projeto é pensar em uma **mini fábrica de ML**:

- `data_utils.py` fabrica a matéria-prima  
- `train.py` treina a máquina  
- `artifacts/model.pkl` é a máquina pronta e empacotada  
- `model_utils.py` busca essa máquina no depósito  
- `routers/predict.py` é o balcão que usa a máquina para responder  
- `main.py` é a recepção principal da API  

Assim, o projeto mostra não apenas o treinamento de um modelo, mas o caminho para transformá-lo em algo utilizável por uma aplicação.

---

## Estrutura do projeto

```bash
aula_02_e03_mlops_dados_sinteticos/
├── notebook/
│   └── e03_dados_sinteticos.ipynb
├── main.py
├── data_utils.py
├── model_utils.py
├── train.py
├── README.md
├── requirements.txt
├── .env.example
├── routers/
│   ├── __init__.py
│   └── predict.py
└── artifacts/
    ├── model.pkl
    ├── model_card.md
    └── requirements_model.txt

##Tecnologias utilizadas

Python
FastAPI
Uvicorn
NumPy
Pandas
Scikit-learn
Joblib
Hugging Face Hub
Objetivos da aula

## Ao final desta atividade, a aplicação contempla:

geração de dataset sintético com sentido de domínio
uso de função reutilizável para criação de dados
treino de modelo de classificação com RandomForestClassifier
avaliação com classification_report
serialização do artefato com joblib
publicação de modelo em repositório do Hugging Face
carregamento remoto do modelo com hf_hub_download
serving do modelo com FastAPI
endpoint de predição
endpoint de health check
Como rodar o projeto
1. Entrar na pasta da aula
cd /workspaces/Projeto_1_CD2/aula_02_e03_mlops_dados_sinteticos
2. Instalar as dependências
python -m pip install -r requirements.txt
3. Treinar o modelo e gerar os artefatos
python train.py
Resultado esperado

## Ao rodar o treino, o terminal deve mostrar:

o classification_report
a criação do arquivo artifacts/model.pkl
a validação do ciclo salvar → carregar → predizer
a criação de:
artifacts/model_card.md
artifacts/requirements_model.txt
Como configurar o Hugging Face
1. Fazer login no terminal
hf auth login

Depois confirmar:

hf auth whoami

O esperado é que apareça seu usuário do Hugging Face.

2. Criar ou confirmar o repositório do modelo

Neste projeto, o repositório utilizado foi:

anaclaragr05/mlops-fraud-v1

Você pode abrir no navegador para verificar:

https://huggingface.co/anaclaragr05/mlops-fraud-v1
3. Confirmar que o repositório contém os arquivos

## O repositório do modelo deve conter:

model.pkl
README.md
requirements.txt
Como rodar a API

Antes de subir a API, configure a variável de ambiente com o repositório do modelo:

export HF_REPO_ID=anaclaragr05/mlops-fraud-v1

Se o repositório for privado, também exporte o token:

export HF_TOKEN=SEU_TOKEN_AQUI

Agora suba a aplicação:

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
Resultado esperado

## No terminal, deve aparecer algo parecido com:

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
Como acessar no navegador

No Codespaces, abra a porta 8000 e use o link gerado.

Rotas principais
Raiz da API
https://SEU_LINK/

Retorno esperado:

{
  "message": "API de ML no ar",
  "projeto": "Aula 2 - e03 dados sintéticos"
}
Documentação Swagger
https://SEU_LINK/docs
Health check
https://SEU_LINK/ml/health

Se tudo estiver correto, o retorno deve ser parecido com:

{
  "api": "ok",
  "model": "ok",
  "model_repo": "anaclaragr05/mlops-fraud-v1"
}
Como testar a predição

A forma mais fácil é pelo Swagger em /docs.

Abra a rota POST /ml/predict, clique em Try it out e teste com os exemplos abaixo.

Exemplo 1 — caso provavelmente legítimo
{
  "valor_transacao": 80,
  "hora_transacao": 14,
  "distancia_ultima_compra": 5,
  "tentativas_senha": 1,
  "pais_diferente": 0
}

Resultado esperado: alta chance de retornar label: "legitimo".

Exemplo 2 — caso provavelmente fraude
{
  "valor_transacao": 8000,
  "hora_transacao": 2,
  "distancia_ultima_compra": 2000,
  "tentativas_senha": 7,
  "pais_diferente": 1
}

Resultado esperado: alta chance de retornar label: "fraude".

Endpoints disponíveis
GET /

Retorna uma mensagem simples indicando que a API está no ar.

GET /ml/health

Verifica se:

a API está funcionando
o modelo foi carregado corretamente
o repositório remoto está acessível
POST /ml/predict

Recebe as features de uma transação e retorna:

prediction
probability
label
model_version
O que cada arquivo faz
data_utils.py

Responsável por gerar o dataset sintético com variáveis coerentes com o domínio de fraude.

train.py

Executa:

geração de dados
split treino/teste
treino do modelo
avaliação
serialização
criação dos artefatos auxiliares
model_utils.py

Responsável por baixar e carregar o modelo do Hugging Face Hub.

routers/predict.py

Define:

o schema de entrada
o endpoint /predict
o endpoint /health
main.py

Inicializa a aplicação FastAPI e registra o router principal.

O que foi aprendido nesta aula

Esta atividade permitiu praticar várias etapas importantes de um pipeline de ML aplicado:

criação de dados sintéticos com reprodutibilidade
transformação de um experimento em função reutilizável
treino e avaliação de modelo supervisionado
serialização do artefato para uso futuro
versionamento do modelo em um repositório remoto
integração do artefato com uma API
separação de responsabilidades em arquivos organizados
Como saber se está tudo certo

Você cumpriu a proposta da aula se conseguir validar os pontos abaixo:

o train.py roda sem erro
artifacts/model.pkl foi criado
o repositório do Hugging Face existe
o modelo foi publicado
/docs abre corretamente
/ml/health retorna model: ok
/ml/predict responde a exemplos válidos
entradas inválidas retornam erro de validação
Problemas comuns
Repository Not Found

Normalmente significa:

HF_REPO_ID errado
nome do repositório incorreto
repositório ainda sem model.pkl
repositório privado sem token
model: degraded no /health

Significa que a API subiu, mas o modelo não foi carregado corretamente.

422 Unprocessable Entity

Significa que o JSON enviado para /predict não respeita as validações do schema.

##Conclusão

Esta aula representa um fluxo simplificado, mas bastante didático, de MLOps aplicado. Em vez de parar no treinamento do modelo, o projeto mostra como transformar esse modelo em um artefato versionado e consumível por uma API.

Mais do que treinar um classificador, o foco aqui foi entender o caminho completo:

dados → modelo → artefato → hub → API → predição