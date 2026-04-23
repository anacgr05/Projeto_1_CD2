from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

from models.bebida import BebidaInput, BebidaOutput

router = APIRouter()

bebidas = [
    {"id": 1, "nome": "Água sem gás", "tipo": "agua", "preco": 6.0, "alcoolica": False, "volume_ml": 500, "criado_em": "2026-01-01T12:00:00"},
    {"id": 2, "nome": "Suco de uva", "tipo": "suco", "preco": 12.0, "alcoolica": False, "volume_ml": 300, "criado_em": "2026-01-01T12:00:00"},
    {"id": 3, "nome": "Refrigerante", "tipo": "refrigerante", "preco": 9.0, "alcoolica": False, "volume_ml": 350, "criado_em": "2026-01-01T12:00:00"},
    {"id": 4, "nome": "Cerveja Pilsen", "tipo": "cerveja", "preco": 15.0, "alcoolica": True, "volume_ml": 600, "criado_em": "2026-01-01T12:00:00"},
    {"id": 5, "nome": "Vinho tinto", "tipo": "vinho", "preco": 29.0, "alcoolica": True, "volume_ml": 150, "criado_em": "2026-01-01T12:00:00"},
]

@router.get("/")
async def listar_bebidas(tipo: Optional[str] = None, alcoolica: Optional[bool] = None):
    resultado = bebidas

    if tipo:
        resultado = [b for b in resultado if b["tipo"] == tipo]

    if alcoolica is not None:
        resultado = [b for b in resultado if b["alcoolica"] == alcoolica]

    return resultado


@router.get("/{bebida_id}")
async def buscar_bebida(bebida_id: int):
    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            return bebida
    raise HTTPException(status_code=404, detail=f"Bebida com id {bebida_id} não encontrada")


@router.post("/", response_model=BebidaOutput, status_code=201)
async def criar_bebida(bebida: BebidaInput):
    novo_id = max(b["id"] for b in bebidas) + 1 if bebidas else 1
    nova_bebida = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **bebida.model_dump()
    }
    bebidas.append(nova_bebida)
    return nova_bebida