from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import Optional

from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas = []


@router.post("/", response_model=ReservaOutput, status_code=201)
async def criar_reserva(reserva: ReservaInput):
    data_hora_reserva = datetime.fromisoformat(reserva.data_hora)

    if data_hora_reserva < datetime.now() + timedelta(hours=1):
        raise HTTPException(
            status_code=400,
            detail="Reservas devem ser feitas com pelo menos 1 hora de antecedência"
        )

    for r in reservas:
        mesma_mesa = r["mesa"] == reserva.mesa
        mesmo_dia = datetime.fromisoformat(r["data_hora"]).date() == data_hora_reserva.date()
        ativa = r["status"] == "ativa"

        if mesma_mesa and mesmo_dia and ativa:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma reserva ativa para essa mesa nesse dia"
            )

    nova_reserva = {
        "id": len(reservas) + 1,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora,
        "status": "ativa"
    }
    reservas.append(nova_reserva)
    return nova_reserva


@router.get("/")
async def listar_reservas(data: Optional[str] = None, status: Optional[str] = None):
    resultado = reservas

    if data:
        resultado = [r for r in resultado if datetime.fromisoformat(r["data_hora"]).date().isoformat() == data]

    if status:
        resultado = [r for r in resultado if r["status"] == status]
    else:
        resultado = [r for r in resultado if r["status"] != "cancelada"]

    return resultado


@router.get("/{reserva_id}")
async def buscar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            reserva["status"] = "cancelada"
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.get("/mesa/{numero}")
async def listar_reservas_por_mesa(numero: int):
    return [r for r in reservas if r["mesa"] == numero]