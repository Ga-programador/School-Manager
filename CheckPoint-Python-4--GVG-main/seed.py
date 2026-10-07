from app.database import SessionLocal, engine, Base
from app.models import Aluno, Professor, Disciplina, Turma, Matricula, Nota, Frequencia

# Apaga as tabelas antigas e recria do zero
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    print("A popular o banco de dados...")

    # 1. Alunos
    a1 = Aluno(nome="Ana Clara Martins", email="ana.martins@email.com", cpf="12345678901")
    a2 = Aluno(nome="Bruno Silva Santos", email="bruno.silva@email.com", cpf="23456789012")
    a3 = Aluno(nome="Carla Mendes Oliveira", email="carla.mendes@email.com", cpf="34567890123")
    a4 = Aluno(nome="Daniel Pereira Lima", email="daniel.lima@email.com", cpf="45678901234")
    
    db.add_all([a1, a2, a3, a4])
    db.commit()

    # 2. Professores
    p1 = Professor(nome="Carlos Eduardo", email="carlos@escola.com")
    p2 = Professor(nome="Mariana Costa", email="mariana@escola.com")
    db.add_all([p1, p2])
    db.commit()

    # 3. Disciplinas
    d1 = Disciplina(nome="Matemática", carga_horaria=80)
    d2 = Disciplina(nome="Português", carga_horaria=80)
    d3 = Disciplina(nome="Python", carga_horaria=60)
    d4 = Disciplina(nome="História", carga_horaria=40)
    db.add_all([d1, d2, d3, d4])
    db.commit()

    # 4. Turmas
    t1 = Turma(nome="Turma A1", ano_letivo=2026, disciplina_id=d1.id, professor_id=p1.id)
    t2 = Turma(nome="Turma B1", ano_letivo=2026, disciplina_id=d3.id, professor_id=p2.id)
    db.add_all([t1, t2])
    db.commit()

    # 5. Matrículas
    m1 = Matricula(aluno_id=a1.id, turma_id=t1.id)
    m2 = Matricula(aluno_id=a2.id, turma_id=t1.id)
    m3 = Matricula(aluno_id=a3.id, turma_id=t2.id)
    m4 = Matricula(aluno_id=a4.id, turma_id=t2.id)
    db.add_all([m1, m2, m3, m4])
    db.commit()

    # 6. Notas
    n1 = Nota(aluno_id=a1.id, turma_id=t1.id, valor=9.5)
    n2 = Nota(aluno_id=a1.id, turma_id=t2.id, valor=8.8)
    n3 = Nota(aluno_id=a2.id, turma_id=t1.id, valor=5.0)
    n4 = Nota(aluno_id=a3.id, turma_id=t2.id, valor=4.5)
    db.add_all([n1, n2, n3, n4])
    db.commit()

    # 7. Frequências (passando aulas_totais e aulas_presentes)
    f1 = Frequencia(aluno_id=a1.id, turma_id=t1.id, aulas_totais=40, aulas_presentes=38)
    f2 = Frequencia(aluno_id=a2.id, turma_id=t1.id, aulas_totais=40, aulas_presentes=32)
    f3 = Frequencia(aluno_id=a3.id, turma_id=t2.id, aulas_totais=40, aulas_presentes=24)
    f4 = Frequencia(aluno_id=a4.id, turma_id=t2.id, aulas_totais=40, aulas_presentes=36)
    db.add_all([f1, f2, f3, f4])
    db.commit()

    print("Banco de dados populado com sucesso!")

except Exception as e:
    print(f"Erro ao popular o banco: {e}")
    db.rollback()
finally:
    db.close()