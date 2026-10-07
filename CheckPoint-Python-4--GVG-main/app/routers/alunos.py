from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.get("", response_model=list[schemas.AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(models.Aluno).all()


@router.get("/{aluno_id}", response_model=schemas.AlunoResponse)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.get(models.Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")
    return aluno


@router.post("", response_model=schemas.AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(dados: schemas.AlunoCreate, db: Session = Depends(get_db)):
    # RN01 - cadastro único (e-mail não pode se repetir)
    existente = db.query(models.Aluno).filter(models.Aluno.email == dados.email).first()
    if existente:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Já existe um aluno com esse e-mail")

    aluno = models.Aluno(**dados.model_dump())
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


@router.put("/{aluno_id}", response_model=schemas.AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.get(models.Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")

    duplicado = (
        db.query(models.Aluno)
        .filter(models.Aluno.email == dados.email, models.Aluno.id != aluno_id)
        .first()
    )
    if duplicado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Já existe um aluno com esse e-mail")

    for campo, valor in dados.model_dump().items():
        setattr(aluno, campo, valor)
    db.commit()
    db.refresh(aluno)
    return aluno


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.get(models.Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")

    tem_vinculos = aluno.matriculas or aluno.notas or aluno.frequencias
    if tem_vinculos:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível excluir o aluno: existem matrículas, notas ou frequências vinculadas",
        )

    db.delete(aluno)
    db.commit()
    return None
