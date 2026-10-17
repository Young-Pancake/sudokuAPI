from ..env_variables import DB_KEY 
from ..dependencies import require_api_key
from ..services.tools import seed_to_index, generate_sudoku
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import INTEGER, ARRAY

class Sudoku(SQLModel, table=True):
    __tablename__ = "puzzles"
    id: int | None = Field(default=None, primary_key=True)
    puzzle: list[list[int]] = Field(sa_column=Column(ARRAY(INTEGER, dimensions=2)))
    puzzle_solved: list[list[int]] = Field(sa_column=Column(ARRAY(INTEGER, dimensions=2)))
    difficulty: str

class SudokuUpdate(SQLModel):
    puzzle: list[list[int]] | None = None
    puzzle_solved: list[list[int]] | None = None
    difficulty: str | None = None

class SudokuSeed(SQLModel):
    seed: int
    difficulty: str

class SudokuRead(SQLModel):
    id: int
    puzzle: list[list[int]]
    puzzle_solved: list[list[int]]
    difficulty: str
    
pg_address = str(DB_KEY)
engine = create_engine(pg_address, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/sudokus/", response_model=SudokuRead, dependencies=[Depends(require_api_key)])
async def create_sudoku(sudoku: Sudoku, session: SessionDep) -> Sudoku:
    session.add(sudoku)
    session.commit()
    session.refresh(sudoku)
    return sudoku


@router.post("/sudokus/generate", response_model=list[SudokuRead], dependencies=[Depends(require_api_key)])
def generate_daily_puzzles(session: SessionDep):
    created = []
    for difficulty in ("easy", "medium", "hard"):
        for _ in range(10):
            data = generate_sudoku(difficulty)
            exists = session.exec(
                select(Sudoku).where(Sudoku.puzzle == data["puzzle"])
            ).first()
            if exists is None:
                sudoku = Sudoku(**data)
                session.add(sudoku)
                session.commit()
                session.refresh(sudoku)
                created.append(sudoku)
                break
        else:
            raise HTTPException(
                status_code=500,
                detail=f"could not generate a new {difficulty} puzzle",
            )
    return created

@router.get("/sudokus/", response_model=list[SudokuRead])
async def read_sudokus(session: SessionDep):
    sudokus = session.exec(select(Sudoku)).all()
    return sudokus

@router.get("/sudokus/seed", response_model=SudokuRead)
async def read_sudoku_by_seed(difficulty_and_seed: Annotated[SudokuSeed, Query()], session: SessionDep):
    count = session.exec(
    select(func.count()).where(Sudoku.difficulty == difficulty_and_seed.difficulty)
    ).one()
    if count == 0:
        raise HTTPException(status_code=404, detail="no puzzles for this difficulty")

    index = seed_to_index(difficulty_and_seed.seed, count)
    answer = session.exec(select(Sudoku)
                 .where(Sudoku.difficulty == difficulty_and_seed.difficulty)
                 .order_by(Sudoku.id).offset(index).limit(1)).first()
    return answer

@router.get("/sudokus/{sudoku_id}", response_model=SudokuRead)
async def read_sudoku(sudoku_id: int, session: SessionDep):
    sudoku = session.get(Sudoku, sudoku_id)
    if not sudoku:
        raise HTTPException(status_code=404, detail="puzzle not found")
    return sudoku

@router.put("/sudokus/{sudoku_id}", response_model=SudokuRead, dependencies=[Depends(require_api_key)])
async def update_sudoku(
    sudoku_id: int,
    update: SudokuUpdate,
    session: SessionDep,
):
    sudoku = session.get(Sudoku, sudoku_id)
    if not sudoku:
        raise HTTPException(status_code=404, detail="puzzle not found")
    for key, val in update.model_dump(exclude_unset=True).items():
        setattr(sudoku, key, val)
    
    session.add(sudoku)
    session.commit()
    session.refresh(sudoku)
    return sudoku

@router.delete("/sudokus/{sudoku_id}", dependencies=[Depends(require_api_key)])
async def delete_sudoku(sudoku_id: int, session: SessionDep):
    sudoku = session.get(Sudoku, sudoku_id)
    if not sudoku:
        raise HTTPException(status_code=404, detail="puzzle not found")
    session.delete(sudoku)
    session.commit()
    return {"ok": sudoku.id}