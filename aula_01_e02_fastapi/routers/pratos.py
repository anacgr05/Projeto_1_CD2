from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from models.prato import PratoInput, PratoOutput, DisponibilidadeInput

router = APIRouter()

pratos = [
    {
        "id": 1,
        "nome": "Pizza Portuguesa",
        "categoria": "pizza",
        "preco": 59.9,
        "preco_promocional": None,
        "descricao": "Pizza Clássica Portuguesa",
        "disponivel": True,
        "criado_em": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "nome": "Nhoque ao Sugo",
        "categoria": "massa",
        "preco": 44.9,
        "preco_promocional": None,
        "descricao": "Massa ao sugo",
        "disponivel": True,
        "criado_em": "2024-01-01T00:00:00"
    },
    {
        "id": 3,
        "nome": "Pudim de Leite",
        "categoria": "sobremesa",
        "preco": 16.9,
        "preco_promocional": None,
        "descricao": "Sobremesa de pudim",
        "disponivel": True,
        "criado_em": "2024-01-01T00:00:00"
    }
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
                return {
                    "nome": prato["nome"],
                    "preco": prato["preco"],
                    "preco_promocional": prato["preco_promocional"]
                }
            return prato

    raise HTTPException(
        status_code=404,
        detail=f"Prato com id {prato_id} não encontrado"
    )


@router.post("/", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    novo_id = max((p["id"] for p in pratos), default=0) + 1
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


@router.post("/{prato_id}/aplicar_desconto")
async def aplicar_desconto(prato_id: int, percentual: float):
    prato = next((p for p in pratos if p["id"] == prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if percentual <= 0 or percentual > 50:
        raise HTTPException(
            status_code=400,
            detail="Percentual de desconto deve estar entre 1% e 50%"
        )

    if not prato["disponivel"]:
        raise HTTPException(
            status_code=400,
            detail="Não é possível aplicar desconto em prato indisponível"
        )

    prato["preco_promocional"] = round(prato["preco"] * (1 - percentual / 100), 2)

    return {
        "mensagem": "Desconto aplicado com sucesso",
        "prato": prato
    }