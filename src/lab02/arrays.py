# arrays.py

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
        out.extend(row) #добавление элементов в конец списка
    return out

#min_max
#print(min_max([3, -1, 5, 5, 0]))
#print(min_max([42]))
#print(min_max([-5, -2, -9]))
#print(min_max([]))
#print("case4")
#print(min_max([1.5, 2, 2.0, -3.1]))
print()

#unique_sorted
#print(unique_sorted([3, 1, 2, 1, 3]))
#print(unique_sorted([]))
#print(unique_sorted([-1, -1, 0, 2, 2]))
#print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
#print()

#flatten
#print(flatten([[1, 2], [3, 4]]))
#print(flatten(([1, 2], (3, 4, 5))))
#print(flatten([[1], [], [2, 3]]))
#print("case4")
print(flatten([[1, 2], "ab"]))
