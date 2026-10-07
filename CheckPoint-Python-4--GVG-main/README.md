SchoolManager

## Descrição
SchoolManager é uma API REST desenvolvida para o Checkpoint 1 (CP1), com o
objetivo de centralizar as principais informações de uma escola: alunos,
professores, turmas, disciplinas, matrículas, notas e frequência.

## Problema escolhido
Escolas costumam lidar com muitas informações espalhadas (alunos, professores,
turmas, disciplinas, notas, frequência), o que gera erros, dados duplicados e
dificuldade para encontrar informações quando não existe um sistema único.

## Solução proposta
Um backend em Python (FastAPI) que centraliza o cadastro dessas entidades e
disponibiliza uma API REST para que administração, secretaria, professores e
alunos possam gerenciar essas informações de forma organizada, com regras de
negócio que evitam dados duplicados ou inconsistentes.

## Integrantes
- Gustavo
- Enzo Gabriel Lima Miranda

## Tecnologias utilizadas
- **Python 3.11+**
- **FastAPI** — construção da API REST
- **SQLAlchemy** — ORM / persistência
- **SQLite** (padrão, sem configuração) ou **Oracle** (opcional, via variável de ambiente)
- **Pydantic** — validação de dados
- **Swagger / OpenAPI** — gerado automaticamente pelo FastAPI

``bash
uvicorn app.main:app --reload
```

A API sobe em: `http://localhost:8000`

## Documentação Swagger
Com o servidor rodando, acesse:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Banco de dados
Por padrão o projeto usa **SQLite** (arquivo `escola.db`, criado automaticamente
na primeira execução — nenhuma configuração extra é necessária). A conexão pode
ser trocada para **Oracle** apenas alterando a variável `DATABASE_URL` no `.env`,
sem precisar mudar o código.

## Execução dos Testes Automatizados

Para executar a suíte de testes unitários e de integração das rotas do projeto, utilize os comandos abaixo no terminal:

1. Certifique-se de que o ambiente virtual está ativo:
   ```powershell
   .\venv\Scripts\Activate.ps1