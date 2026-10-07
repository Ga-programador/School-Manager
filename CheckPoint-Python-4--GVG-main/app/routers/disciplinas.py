from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])


@router.get("", response_model=list[schemas.DisciplinaResponse])
def listar_disciplinas(db: Session = Depends(get_db)):
    return db.query(models.Disciplina).all()


@router.get("/{disciplina_id}", response_model=schemas.DisciplinaResponse)
def obter_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.get(models.Disciplina, disciplina_id)
    if not disciplina:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disciplina não encontrada")
    return disciplina


@router.post("", response_model=schemas.DisciplinaResponse, status_code=status.HTTP_201_CREATED)
def criar_disciplina(dados: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    disciplina = models.Disciplina(**dados.model_dump())
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina


@router.put("/{disciplina_id}", response_model=schemas.DisciplinaResponse)
def atualizar_disciplina(
    disciplina_id: int, dados: schemas.DisciplinaUpdate, db: Session = Depends(get_db)
):
    disciplina = db.get(models.Disciplina, disciplina_id)
    if not disciplina:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disciplina não encontrada")

    for campo, valor in dados.model_dump().items():
        setattr(disciplina, campo, valor)
    db.commit()
    db.refresh(disciplina)
    return disciplina


@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.get(models.Disciplina, disciplina_id)
    if not disciplina:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disciplina não encontrada")

    # RN07 - a exclusão respeita os relacionamentos existentes
    if disciplina.turmas or disciplina.notas:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível excluir a disciplina: existem turmas ou notas vinculadas",
        )

    db.delete(disciplina)
    db.commit()
    return None
