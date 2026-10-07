from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


#aluno
class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    data_nascimento: Optional[date] = None


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(AlunoBase):
    pass


class AlunoResponse(AlunoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


#profs
class ProfessorBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    email: EmailStr


class ProfessorCreate(ProfessorBase):
    pass


class ProfessorUpdate(ProfessorBase):
    pass


class ProfessorResponse(ProfessorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


#disciplina
class DisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    carga_horaria: Optional[int] = Field(default=None, ge=1)


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaUpdate(DisciplinaBase):
    pass


class DisciplinaResponse(DisciplinaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


#turma
class TurmaBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    disciplina_id: int
    professor_id: Optional[int] = None


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(TurmaBase):
    pass


class TurmaResponse(TurmaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


#matricula
class MatriculaBase(BaseModel):
    aluno_id: int
    turma_id: int


class MatriculaCreate(MatriculaBase):
    pass


class MatriculaResponse(MatriculaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data_matricula: datetime


#notas
class NotaBase(BaseModel):
    aluno_id: int
    disciplina_id: int
    valor: float = Field(..., ge=0, le=10, description="Nota entre 0 e 10")


class NotaCreate(NotaBase):
    pass


class NotaUpdate(BaseModel):
    valor: float = Field(..., ge=0, le=10, description="Nota entre 0 e 10")


class NotaResponse(NotaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


#frequencia
class FrequenciaBase(BaseModel):
    aluno_id: int
    turma_id: int
    data: date = Field(default_factory=date.today)
    presente: bool = True

class FrequenciaCreate(FrequenciaBase):
    pass

class FrequenciaUpdate(BaseModel):
    presente: bool

class FrequenciaResponse(FrequenciaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
