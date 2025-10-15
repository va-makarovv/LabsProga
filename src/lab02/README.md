# Лабораторная работа 2
## ЗАДАНИЕ A - ARRAYS.PY

```python
from typing import Union

Number = Union[float, int]


def min_max(nums: list[Number]) -> tuple[Number, Number]:
    """
    Вернуть кортеж (минимум, максимум).
    Если список пуст — ValueError.
    """
    if not nums:
        raise ValueError("nums must not be empty")
    return (min(nums), max(nums))


def unique_sorted(nums: list[Number]) -> list[Number]:
    """
    Вернуть отсортированный список уникальных значений (по возрастанию).
    Допускается смешение int/float: 1 и 1.0 считаются одним значением.
    """
    return sorted(set(nums))


def flatten(mat: list[list | tuple] | tuple[list | tuple, ...]) -> list:
    """
    «Расплющить» список списков/кортежей в один список по строкам (row-major).
    Если встретилась строка/элемент, который не является списком/кортежем — TypeError.
    """
    out: list = []
    for i, row in enumerate(mat):
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"row {i} is not a list or tuple")
        out.extend(row)
    return out

#min_max
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
#print(min_max([]))
print(min_max([1.5, 2, 2.0, -3.1]))
print()

#unique_sorted
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
print()

#flatten
print(flatten([[1, 2], [3, 4]]))
print(flatten(([1, 2], (3, 4, 5))))
print(flatten([[1], [], [2, 3]]))
#print(flatten([[1, 2], "ab"]))
```
![](/images/lab02/arrays01.png)
![](/images/lab02/arrays02.png)
![](/images/lab02/arrays03.png)


## ЗАДАНИЕ B - MATRIX.PY

```python
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
    return [list(col) for col in zip(*mat)]


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

#transpose
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
# print(transpose([[1, 2], [3]]))
print()

#row_sums
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
# print(row_sums([[1, 2], [3]]))
print()

#col_sums
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
# print(col_sums([[1, 2], [3]]))
print()
```
![](/images/lab02/matrix01.png)
![](/images/lab02/matrix02.png)
![](/images/lab02/matrix03.png)
![](/images/lab02/matrix04.png)

## ЗАДАНИЕ C - TUPLES.PY

```python
rec1 = ("Иванов Иван Иванович", "BIVT-25", 4.6)
rec2 = ("Петров Пётр", "IKBO-12", 5.0)
rec3 = ("Петров Пётр Петрович", "IKBO-12", 5.0)
rec4 = (" сидорова анна сергеевна ", "ABB-01", 3.999)
rec5 = ("", "ABB-01", 3.999)

def fio(rec):
    part = rec[0].split()
    if not part:
        raise ValueError("FIO is empty")
    init = ''.join(l[0].upper() for l in part[1:])
    surn = part[0][0].upper() + part[0][1:]
    return f"{surn} {'.'.join(init)}."

def gpa(rec):
    gp = rec[2]
    if not gp:
        raise ValueError("GPA is empty")
    else:
        return round(rec[2], 2)


def formatRec(rec):
    if len(rec) != 3:
        raise ValueError("Wrong data")
    else:
        name = fio(rec)
        gr = rec[1]
        if not gr:
            raise ValueError("Group is empty")
        gp = gpa(rec)
        print(f"{name}, гр. {gr}, GPA: {gp}")

formatRec(rec1)
formatRec(rec2)
formatRec(rec3)
formatRec(rec4)
formatRec(rec5)

```

![](/images/lab02/tuples.png)
