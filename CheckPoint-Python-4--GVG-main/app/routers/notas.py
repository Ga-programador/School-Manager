from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/notas", tags=["Notas"])


@router.get("", response_model=list[schemas.NotaResponse])
def listar_notas(db: Session = Depends(get_db)):
    return db.query(models.Nota).all()

@router.get("/{nota_id}", response_model=schemas.NotaResponse)
def obter_nota(nota_id: int, db: Session = Depends(get_db)):
    nota = db.get(models.Nota, nota_id)
    if not nota:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nota não encontrada")
    return nota

@router.post("", response_model=schemas.NotaResponse, status_code=status.HTTP_201_CREATED)
def criar_nota(dados: schemas.NotaCreate, db: Session = Depends(get_db)):
    #não é possível lançar nota para aluno ou disciplina inexistente
    if not db.get(models.Aluno, dados.aluno_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno informado não existe")
    if not db.get(models.Disciplina, dados.disciplina_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disciplina informada não existe")

    #o valor já é validado pelo schema
    nota = models.Nota(**dados.model_dump())
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota


@router.put("/{nota_id}", response_model=schemas.NotaResponse)
def atualizar_nota(nota_id: int, dados: schemas.NotaUpdate, db: Session = Depends(get_db)):
    nota = db.get(models.Nota, nota_id)
    if not nota:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nota não encontrada")

    nota.valor = dados.valor
    db.commit()
    db.refresh(nota)
    return nota


@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_nota(nota_id: int, db: Session = Depends(get_db)):
    nota = db.get(models.Nota, nota_id)
    if not nota:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nota não encontrada")

    db.delete(nota)
    db.commit()
    return None
