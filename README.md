# sudokuapi

A Sudoku puzzle API built with FastAPI, SQLModel, and PostgreSQL. 
check it out at [sudokuapi](https://sudokuapi.fastapicloud.dev/docs)

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL 14 or newer, locally or hosted

## 1. Install dependencies

```bash
uv sync
```

## 2. Create the database

With a local PostgreSQL server:

```bash
psql -U postgres -c "CREATE DATABASE sudoku_db;"
```

## 3. Create the table

```bash
psql -U postgres -d sudoku_db -f schemas/sudoku.sql
```

## 4. Modify the .env.example file and then:

```bash
mv .env.example .env
```

## 5. Run the API

```bash
uv run fastapi dev
```

## Endpoints

| Method | Route | Key required | Purpose |
|--------|-------|--------------|---------|
| GET | `/sudokus/` | No | List all puzzles |
| GET | `/sudokus/{id}` | No | Get one puzzle by id |
| GET | `/sudokus/seed?difficulty=easy&seed=42` | No | Get a puzzle chosen by seed |
| POST | `/sudokus/` | Yes | Create a puzzle from a body |
| POST | `/sudokus/generate/{difficulty}` | Yes | Generate and store one puzzle |
| PUT | `/sudokus/{id}` | Yes | Update fields of a puzzle |
| DELETE | `/sudokus/{id}` | Yes | Delete a puzzle |

