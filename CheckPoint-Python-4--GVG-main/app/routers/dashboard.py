from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Função de dependência para verificar se é Admin ou Professor
def verificar_acesso_admin(x_user_role: str = Header(default="admin")):
    if x_user_role.lower() not in ["admin", "professor"]:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Perfil não autorizado a visualizar métricas restritas."
        )
    return x_user_role

@router.get("/metricas")
def obter_metricas_dashboard(
    db: Session = Depends(get_db),
    role: str = Depends(verificar_acesso_admin)
):
    total_alunos = db.query(models.Aluno).count()
    total_turmas = db.query(models.Turma).count()
    
    media_geral = db.query(func.avg(models.Nota.valor)).scalar() or 0.0
    
    alunos_em_risco = (
        db.query(models.Nota.aluno_id)
        .group_by(models.Nota.aluno_id)
        .having(func.avg(models.Nota.valor) < 6.0)
        .count()
    )

    return {
        "total_alunos": total_alunos,
        "total_turmas": total_turmas,
        "media_geral_escola": round(media_geral, 2),
        "alunos_em_risco": alunos_em_risco
    }