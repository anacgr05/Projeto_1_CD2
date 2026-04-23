# e04 — Aula 3

Esta pasta reúne os materiais da Aula 3.

## Parte 1 — GitHub Actions
Nesta primeira parte, o foco é criar um workflow de Integração Contínua (CI) com GitHub Actions para validar automaticamente a API Bella Tavola desenvolvida anteriormente.

## Estrutura usada
- API alvo: `aula_01_e02_fastapi`
- Workflow: `.github/workflows/ci.yml`

## O que o workflow faz
- baixa o código
- configura Python 3.11
- instala as dependências
- sobe a API
- testa a rota `/`