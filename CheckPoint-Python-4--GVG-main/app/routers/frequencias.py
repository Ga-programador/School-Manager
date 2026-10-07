from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/frequencias", tags=["Frequências"])


@router.get("", response_model=list[schemas.FrequenciaResponse])
def listar_frequencias(db: Session = Depends(get_db)):
    return db.query(models.Frequencia).all()


@router.get("/{frequencia_id}", response_model=schemas.FrequenciaResponse)
def obter_frequencia(frequencia_id: int, db: Session = Depends(get_db)):
    frequencia = db.get(models.Frequencia, frequencia_id)
    if not frequencia:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Frequência não encontrada")
    return frequencia


@router.post("", response_model=schemas.FrequenciaResponse, status_code=status.HTTP_201_CREATED)
def criar_frequencia(dados: schemas.FrequenciaCreate, db: Session = Depends(get_db)):
    # RN06 - não é possível registrar frequência para aluno ou turma inexistente
    if not db.get(models.Aluno, dados.aluno_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno informado não existe")
    if not db.get(models.Turma, dados.turma_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Turma informada não existe")

    frequencia = models.Frequencia(**dados.model_dump())
    db.add(frequencia)
    db.commit()
    db.refresh(frequencia)
    return frequencia


@router.put("/{frequencia_id}", response_model=schemas.FrequenciaResponse)
def atualizar_frequencia(
    frequencia_id: int, dados: schemas.FrequenciaUpdate, db: Session = Depends(get_db)
):
    frequencia = db.get(models.Frequencia, frequencia_id)
    if not frequencia:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Frequência não encontrada")

    frequencia.presente = dados.presente
    db.commit()
    db.refresh(frequencia)
    return frequencia


@router.delete("/{frequencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_frequencia(frequencia_id: int, db: Session = Depends(get_db)):
    frequencia = db.get(models.Frequencia, frequencia_id)
    if not frequencia:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Frequência não encontrada")

    db.delete(frequencia)
    db.commit()
    return None
