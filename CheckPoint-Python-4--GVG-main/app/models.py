from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    cpf = Column(String, unique=True, nullable=False)
    data_nascimento = Column(String, nullable=True)

    matriculas = relationship("Matricula", back_populates="aluno", cascade="all, delete-orphan")
    notas = relationship("Nota", back_populates="aluno", cascade="all, delete-orphan")
    frequencias = relationship("Frequencia", back_populates="aluno", cascade="all, delete-orphan")

class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    especialidade = Column(String, nullable=True)

    turmas = relationship("Turma", back_populates="professor")

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    carga_horaria = Column(Integer, nullable=False)

    turmas = relationship("Turma", back_populates="disciplina")

class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ano_letivo = Column(Integer, nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id", ondelete="SET NULL"), nullable=True)

    disciplina = relationship("Disciplina", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    matriculas = relationship("Matricula", back_populates="turma", cascade="all, delete-orphan")
    notas = relationship("Nota", back_populates="turma", cascade="all, delete-orphan")
    frequencias = relationship("Frequencia", back_populates="turma", cascade="all, delete-orphan")

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id", ondelete="CASCADE"), nullable=False)
    data_matricula = Column(String, nullable=True)

    aluno = relationship("Aluno", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id", ondelete="CASCADE"), nullable=False)
    valor = Column(Float, CheckConstraint("valor >= 0 AND valor <= 10"), nullable=False)
    descricao = Column(String, nullable=True)

    aluno = relationship("Aluno", back_populates="notas")
    turma = relationship("Turma", back_populates="notas")

class Frequencia(Base):
    __tablename__ = "frequencias"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id", ondelete="CASCADE"), nullable=False)
    aulas_totais = Column(Integer, nullable=False)
    aulas_presentes = Column(Integer, nullable=False)

    aluno = relationship("Aluno", back_populates="frequencias")
    turma = relationship("Turma", back_populates="frequencias")