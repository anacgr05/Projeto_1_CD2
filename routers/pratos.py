from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

from models.prato import PratoInput, PratoOutput, DisponibilidadeInput

router = APIRouter()

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "preco_promocional": None, "descricao": "Molho e muçarela", "disponivel": True, "criado_em": "2026-01-01T12:00:00"},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "preco_promocional": 46.0, "descricao": "Clássica italiana", "disponivel": True, "criado_em": "2026-01-01T12:00:00"},
    {"id": 3, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 24.0, "preco_promocional": None, "descricao": "Sobremesa italiana", "disponivel": True, "criado_em": "2026-01-01T12:00:00"},
]

@router.get("/")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = False
):
    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]

    return resultado


@router.get("/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato

    raise HTTPException(status_code=404, detail=f"Prato com id {prato_id} não encontrado")


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1 if pratos else 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    pratos.append(novo_prato)
    return novo_prato


@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    for prato in pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = body.disponivel
            return prato

    raise HTTPException(status_code=404, detail="Prato não encontrado")