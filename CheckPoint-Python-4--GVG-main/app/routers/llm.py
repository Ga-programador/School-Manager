import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI
from dotenv import load_dotenv
from app.database import get_db
from app import models

load_dotenv()

router = APIRouter(prefix="/llm", tags=["Inteligência Artificial"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@router.post("/relatorio-aluno/{aluno_id}")
def gerar_relatorio_aluno(aluno_id: int, db: Session = Depends(get_db)):
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Chave OPENAI_API_KEY não configurada no ambiente."
        )

    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    notas = db.query(models.Nota).filter(models.Nota.aluno_id == aluno_id).all()
    frequencias = db.query(models.Frequencia).filter(models.Frequencia.aluno_id == aluno_id).all()

    historico_notas = [f"Nota: {n.valor} ({n.descricao or 'Sem descrição'})" for n in notas]
    historico_frequencia = [f"Aulas presentes: {f.aulas_presentes}/{f.aulas_totais}" for f in frequencias]

    prompt = f"""
    Você é um assistente pedagógico escolar. Analise os seguintes dados do aluno e gere um relatório construtivo.

    Aluno: {aluno.nome}
    Notas: {', '.join(historico_notas) if historico_notas else 'Nenhuma nota registrada'}
    Frequência: {', '.join(historico_frequencia) if historico_frequencia else 'Nenhuma frequência registrada'}

    Forneça a resposta estruturada com:
    - Resumo do Desempenho
    - Pontos Fortes
    - Áreas de Atenção
    - Recomendações de Estudo
    """

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "aluno_id": aluno.id,
            "nome": aluno.nome,
            "relatorio_ia": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar OpenAI: {str(e)}")