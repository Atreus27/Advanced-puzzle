from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from app.puzzles.sudoku import Sudoku

app = FastAPI(title="Advanced Puzzle API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

s = Sudoku()

# Simple in-memory leaderboard (for demo)
leaderboard: List[dict] = []

class GenerateRequest(BaseModel):
    difficulty: Optional[str] = "medium"

@app.get("/api/puzzle/sudoku")
async def get_sudoku(difficulty: str = "medium"):
    if difficulty not in {"easy", "medium", "hard", "extreme"}:
        raise HTTPException(status_code=400, detail="Invalid difficulty")
    grid = s.generate(difficulty=difficulty)
    return {"type": "sudoku", "difficulty": difficulty, "grid": grid}

class SolveRequest(BaseModel):
    grid: list

@app.post("/api/puzzle/sudoku/solve")
async def solve_sudoku(payload: SolveRequest):
    grid = payload.grid
    if not isinstance(grid, list) or len(grid) != 9:
        raise HTTPException(status_code=400, detail="Grid must be 9x9 list")
    solution = s.solve([list(map(int, row)) for row in grid])
    if solution is None:
        raise HTTPException(status_code=400, detail="No solution")
    return {"solution": solution}

# Leaderboard
class ScoreEntry(BaseModel):
    name: str
    score: int

@app.get('/api/leaderboard')
async def get_leaderboard(top: int = 10):
    sorted_scores = sorted(leaderboard, key=lambda x: x['score'])
    return {"scores": sorted_scores[:top]}

@app.post('/api/leaderboard')
async def post_leaderboard(entry: ScoreEntry):
    leaderboard.append({"name": entry.name, "score": entry.score})
    leaderboard.sort(key=lambda x: x['score'])
    if len(leaderboard) > 100:
        del leaderboard[100:]
    return {"ok": True}

@app.get("/")
async def ui():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.exception_handler(Exception)
async def generic_exc_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})
