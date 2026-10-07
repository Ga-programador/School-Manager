from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


@router.get("", response_model=list[schemas.MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    return db.query(models.Matricula).all()


@router.get("/{matricula_id}", response_model=schemas.MatriculaResponse)
def obter_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = db.get(models.Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matrícula não encontrada")
    return matricula


@router.post("", response_model=schemas.MatriculaResponse, status_code=status.HTTP_201_CREATED)
def criar_matricula(dados: schemas.MatriculaCreate, db: Session = Depends(get_db)):

    if not db.get(models.Aluno, dados.aluno_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno informado não existe")
    if not db.get(models.Turma, dados.turma_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Turma informada não existe")

#duplicidade de matricula
    duplicada = (
        db.query(models.Matricula)
        .filter(
            models.Matricula.aluno_id == dados.aluno_id,
            models.Matricula.turma_id == dados.turma_id,
        )
        .first()
    )
    if duplicada:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Aluno já está matriculado nessa turma")

    matricula = models.Matricula(**dados.model_dump())
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = db.get(models.Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matrícula não encontrada")

    db.delete(matricula)
    db.commit()
    return None
