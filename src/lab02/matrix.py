from typing import Iterable

Number = float | int


def _check_rectangular(mat: list[list[Number]]) -> tuple[int, int]:
    """
    Проверяет прямоугольность матрицы (все строки одинаковой длины).
    Возвращает (rows, cols) или выбрасывает ValueError для рваной матрицы.
    Пустая матрица [] считается корректной и имеет форму (0, 0).
    """
    if not mat:
        return 0, 0
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError("Матрица рваная: строки разной длины")
    return len(mat), cols


def transpose(mat: list[list[Number]]) -> list[list[Number]]:
    """
    Поменять строки и столбцы местами.
    [] -> []
    Для рваной матрицы -> ValueError.
    """
    _, cols = _check_rectangular(mat)
    if not mat:
        return []
    # zip(*mat) даёт кортежи, приводим к list[list]
    return [list(col) for col in zip(*mat)]  # подаются по строкам, собираются столбцы


def row_sums(mat: list[list[Number]]) -> list[Number]:
    """
    Сумма по каждой строке.
    Требуется прямоугольность (ValueError для рваной матрицы).
    [] -> []
    """
    _check_rectangular(mat)
    return [sum(row) for row in mat]


def col_sums(mat: list[list[Number]]) -> list[Number]:
    """
    Сумма по каждому столбцу.
    Требуется прямоугольность (ValueError для рваной матрицы).
    [] -> []
    """
    rows, cols = _check_rectangular(mat)
    if cols == 0:
        return []
    sums = [0] * cols
    for row in mat:
        for j, val in enumerate(row):
            sums[j] += val
    return sums


# transpose
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
# print(transpose([[1, 2], [3]]))
print()

# row_sums
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
# print(row_sums([[1, 2], [3]]))
print()

# col_sums
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
# print(col_sums([[1, 2], [3]]))
print()
