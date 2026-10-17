import random

def seed_to_index(seed: int, count: int) -> int:
    rng = random.Random(seed)
    return rng.randrange(count)


GIVENS = {"easy": 40, "medium": 32, "hard": 26}


def find_empty(grid: list[list[int]]) -> tuple[int, int] | None:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def is_valid(grid: list[list[int]], r: int, c: int, digit: int) -> bool:
    if digit in grid[r]:
        return False
    if any(grid[i][c] == digit for i in range(9)):
        return False
    box_r, box_c = r // 3 * 3, c // 3 * 3
    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if grid[i][j] == digit:
                return False
    return True


def _fill(grid: list[list[int]], rng: random.Random) -> bool:
    cell = find_empty(grid)
    if cell is None:
        return True
    r, c = cell
    digits = list(range(1, 10))
    rng.shuffle(digits)
    for digit in digits:
        if is_valid(grid, r, c, digit):
            grid[r][c] = digit
            if _fill(grid, rng):
                return True
            grid[r][c] = 0
    return False


def solved_sudoku() -> list[list[int]]:
    grid = [[0] * 9 for _ in range(9)]
    _fill(grid, random.Random())
    return grid


def _count_solutions(grid: list[list[int]]) -> int:
    cell = find_empty(grid)
    if cell is None:
        return 1
    r, c = cell
    total = 0
    for digit in range(1, 10):
        if is_valid(grid, r, c, digit):
            grid[r][c] = digit
            total += _count_solutions(grid)
            grid[r][c] = 0
            if total >= 2:
                return total
    return total


def generate_sudoku(difficulty: str) -> dict:
    target = GIVENS[difficulty]
    rng = random.Random()
    while True:
        solution = solved_sudoku()
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(9) for c in range(9)]
        rng.shuffle(cells)
        givens = 81
        for r, c in cells:
            if givens <= target:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            if _count_solutions(puzzle) == 1:
                givens -= 1
            else:
                puzzle[r][c] = backup
        if givens == target:
            return {
                "puzzle": puzzle,
                "puzzle_solved": solution,
                "difficulty": difficulty,
            }


p = generate_sudoku("easy")
print(p)