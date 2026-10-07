from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/professores", tags=["Professores"])

@router.get("", response_model=list[schemas.ProfessorResponse])
def listar_professores(db: Session = Depends(get_db)):
    return db.query(models.Professor).all()


@router.get("/{professor_id}", response_model=schemas.ProfessorResponse)
def obter_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.get(models.Professor, professor_id)
    if not professor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professor não encontrado")
    return professor


@router.post("", response_model=schemas.ProfessorResponse, status_code=status.HTTP_201_CREATED)
def criar_professor(dados: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    #cadastro único
    existente = db.query(models.Professor).filter(models.Professor.email == dados.email).first()
    if existente:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Já existe um professor com esse e-mail")

    professor = models.Professor(**dados.model_dump())
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor


@router.put("/{professor_id}", response_model=schemas.ProfessorResponse)
def atualizar_professor(
    professor_id: int, dados: schemas.ProfessorUpdate, db: Session = Depends(get_db)
):
    professor = db.get(models.Professor, professor_id)
    if not professor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professor não encontrado")

    duplicado = (
        db.query(models.Professor)
        .filter(models.Professor.email == dados.email, models.Professor.id != professor_id)
        .first()
    )
    if duplicado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Já existe um professor com esse e-mail")

    for campo, valor in dados.model_dump().items():
        setattr(professor, campo, valor)
    db.commit()
    db.refresh(professor)
    return professor


@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.get(models.Professor, professor_id)
    if not professor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professor não encontrado")

    #exclusão respeita os relacionamentos existentes
    if professor.turmas:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível excluir o professor: existem turmas vinculadas a ele",
        )

    db.delete(professor)
    db.commit()
    return None
