# Aula 01 - e02 FastAPI

Este projeto corresponde à primeira aula prática de FastAPI da disciplina, com foco na construção de uma API para o restaurante fictício **Bella Tavola**.

## Objetivo da aula

O objetivo desta atividade foi desenvolver uma API progressivamente, começando com rotas simples e evoluindo para uma estrutura mais organizada e próxima de um projeto real.

Ao final da aula, a aplicação contempla:

- criação de rotas com FastAPI
- uso de métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`)
- uso de path parameters
- uso de query parameters
- envio de dados via body
- validação com Pydantic
- tratamento de erros com `HTTPException`
- padronização de erros com handlers globais
- modularização do projeto com `routers/` e `models/`
- uso de configurações com `config.py` e `.env`

## Analogia do projeto

Uma forma simples de entender este projeto é imaginar um restaurante:

- `main.py` funciona como a **recepção principal**
- `routers/` funciona como os **setores do restaurante**
- `models/` funciona como os **formulários oficiais**
- `config.py` e `.env` funcionam como as **regras da gerência**

Assim, a API foi construída como se fosse a equipe digital do restaurante **Bella Tavola**.

## Estrutura do projeto

```bash
aula_01_e02_fastapi/
├── main.py
├── config.py
├── .env
├── requirements.txt
├── README.md
├── routers/
│   ├── __init__.py
│   ├── pratos.py
│   ├── bebidas.py
│   ├── pedidos.py
│   └── reservas.py
└── models/
    ├── __init__.py
    ├── prato.py
    ├── bebida.py
    ├── pedido.py
    └── reserva.py