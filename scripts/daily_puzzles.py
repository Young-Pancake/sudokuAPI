import json
import os
import subprocess

from sudokuapi.services.tools import generate_sudoku

API_URL = os.environ["API_URL"].rstrip("/")
API_KEY = os.environ["API_KEY"]


def api_request(method, path, body=None):
    cmd = [
        "curl", "-sS", "-f", "--max-time", "60",
        "-X", method,
        f"{API_URL}{path}",
        "-H", f"X-API-Key: {API_KEY}",
    ]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

existing = {tuple(map(tuple, row["puzzle"])) for row in api_request("GET", "/sudokus/")}

for difficulty in ("easy", "medium", "hard"):
    for _ in range(10):
        puzzle = generate_sudoku(difficulty)
        if tuple(map(tuple, puzzle["puzzle"])) not in existing:
            break
    else:
        raise SystemExit(f"could not generate a new {difficulty} puzzle")

    created = api_request("POST", "/sudokus/", puzzle)
    existing.add(tuple(map(tuple, created["puzzle"])))
    print(difficulty, "saved with id", created["id"])