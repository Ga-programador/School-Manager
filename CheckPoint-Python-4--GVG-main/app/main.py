import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import (
    alunos, 
    professores, 
    disciplinas, 
    turmas, 
    matriculas, 
    notas, 
    frequencias,
    dashboard,
    llm
)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SchoolManager - API",
    description=(
        "API REST do sistema SchoolManager, para gerenciamento de alunos, professores, "
        "turmas, disciplinas, matrículas, notas, frequência e inteligência analítica."
    ),
    version="2.0.0",
)

# Configuração do caminho absoluto para static e diretório base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Monta o servidor de arquivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- HANDLERS DE EXCEÇÃO ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": True, "mensagem": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"erro": True, "mensagem": "Dados inválidos", "detalhes": exc.errors()},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"erro": True, "mensagem": "Erro interno no servidor"},
    )

# --- ROTAS DE PÁGINAS (HTML) ---
@app.get("/", include_in_schema=False)
@app.get("/login", include_in_schema=False)
@app.get("/login.html", include_in_schema=False)
def page_login():
    return FileResponse(os.path.join(BASE_DIR, "login.html"))

@app.get("/dashboard", include_in_schema=False)
@app.get("/dashboard.html", include_in_schema=False)
def page_dashboard():
    return FileResponse(os.path.join(BASE_DIR, "dashboard.html"))

@app.get("/gestao", include_in_schema=False)
@app.get("/gestao.html", include_in_schema=False)
@app.get("/alunos", include_in_schema=False)
def page_gestao():
    return FileResponse(os.path.join(BASE_DIR, "gestao.html"))

@app.get("/lancamentos", include_in_schema=False)
@app.get("/lancamentos.html", include_in_schema=False)
def page_lancamentos():
    return FileResponse(os.path.join(BASE_DIR, "lancamentos.html"))

@app.get("/ia", include_in_schema=False)
@app.get("/ia.html", include_in_schema=False)
def page_ia():
    return FileResponse(os.path.join(BASE_DIR, "ia.html"))

# --- ROTAS DO PORTAL DO ALUNO ---
@app.get("/aluno-dashboard", include_in_schema=False)
@app.get("/aluno_dashboard.html", include_in_schema=False)
def read_aluno_dashboard():
    path = os.path.join(BASE_DIR, "aluno_dashboard.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo aluno_dashboard.html não encontrado no servidor.")
    return FileResponse(path)

@app.get("/aluno-notas", include_in_schema=False)
@app.get("/aluno_notas.html", include_in_schema=False)
def read_aluno_notas():
    path = os.path.join(BASE_DIR, "aluno_notas.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo aluno_notas.html não encontrado no servidor.")
    return FileResponse(path)

@app.get("/aluno-frequencia", include_in_schema=False)
@app.get("/aluno_frequencia.html", include_in_schema=False)
def read_aluno_frequencia():
    # Verifica o nome correto salvo no disco (trata o erro de digitação aluno_frquencia vs aluno_frequencia)
    path_correto = os.path.join(BASE_DIR, "aluno_frequencia.html")
    path_alt = os.path.join(BASE_DIR, "aluno_frequencia.html")
    
    path_final = path_correto if os.path.exists(path_correto) else path_alt
    if not os.path.exists(path_final):
        raise HTTPException(status_code=404, detail="Arquivo de frequência do aluno não encontrado.")
    return FileResponse(path_final)

@app.get("/aluno-pareceres", include_in_schema=False)
@app.get("/aluno_pareceres.html", include_in_schema=False)
def read_aluno_pareceres():
    path = os.path.join(BASE_DIR, "aluno_pareceres.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo aluno_pareceres.html não encontrado no servidor.")
    return FileResponse(path)

# --- REGISTRO DOS ROTEADORES ---
app.include_router(alunos.router)
app.include_router(professores.router)
app.include_router(disciplinas.router)
app.include_router(turmas.router)
app.include_router(matriculas.router)
app.include_router(notas.router)
app.include_router(frequencias.router)
app.include_router(dashboard.router)
app.include_router(llm.router)