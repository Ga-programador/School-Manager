from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/turmas", tags=["Turmas"])


def _validar_referencias(dados, db: Session):
    if not db.get(models.Disciplina, dados.disciplina_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disciplina informada não existe")
    if dados.professor_id is not None and not db.get(models.Professor, dados.professor_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professor informado não existe")


@router.get("", response_model=list[schemas.TurmaResponse])
def listar_turmas(db: Session = Depends(get_db)):
    return db.query(models.Turma).all()


@router.get("/{turma_id}", response_model=schemas.TurmaResponse)
def obter_turma(turma_id: int, db: Session = Depends(get_db)):
    turma = db.get(models.Turma, turma_id)
    if not turma:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Turma não encontrada")
    return turma


@router.post("", response_model=schemas.TurmaResponse, status_code=status.HTTP_201_CREATED)
def criar_turma(dados: schemas.TurmaCreate, db: Session = Depends(get_db)):
    _validar_referencias(dados, db)
    turma = models.Turma(**dados.model_dump())
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma


@router.put("/{turma_id}", response_model=schemas.TurmaResponse)
def atualizar_turma(turma_id: int, dados: schemas.TurmaUpdate, db: Session = Depends(get_db)):
    turma = db.get(models.Turma, turma_id)
    if not turma:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Turma não encontrada")

    _validar_referencias(dados, db)
    for campo, valor in dados.model_dump().items():
        setattr(turma, campo, valor)
    db.commit()
    db.refresh(turma)
    return turma


@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_turma(turma_id: int, db: Session = Depends(get_db)):
    turma = db.get(models.Turma, turma_id)
    if not turma:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Turma não encontrada")

    # RN07 - a exclusão respeita os relacionamentos existentes
    if turma.matriculas or turma.frequencias:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível excluir a turma: existem matrículas ou frequências vinculadas",
        )

    db.delete(turma)
    db.commit()
    return None
