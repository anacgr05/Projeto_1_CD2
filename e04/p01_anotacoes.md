# e04 p01 — GitHub Actions

## Objetivo
Criar um workflow de Integração Contínua (CI) para validar automaticamente se a API Bella Tavola continua funcionando após push ou pull request.

## Ideia principal
O workflow executa uma rotina automática:
1. baixa o código
2. configura o Python
3. instala as dependências da API da Aula 1
4. sobe a API com Uvicorn
5. testa se a rota raiz responde

## Analogia
É como um checklist automático de abertura do restaurante:
- preparar a cozinha
- abrir a casa
- confirmar que a recepção atende