# Лабораторная работа 10

## Задание А - structures.py

```python
from __future__ import annotations

from collections import deque
from typing import Any, Deque, Iterable, Iterator, Optional


class Stack:
    """LIFO"""

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        self._data: list[Any] = []
        if iterable is not None:
            self._data.extend(iterable)

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Optional[Any]:
        return self._data[-1] if self._data else None

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"


class Queue:
    """FIFO"""

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        self._data: Deque[Any] = deque()
        if iterable is not None:
            self._data.extend(iterable)

    def enqueue(self, item: Any) -> None:
        self._data.append(item)

    def dequeue(self) -> Any:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self) -> Optional[Any]:
        return self._data[0] if self._data else None

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)!r})"
```

## Задание B - linked_list.py

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Iterator, Optional


@dataclass
class Node:
    value: Any
    next: Optional["Node"] = None


class SinglyLinkedList:
    """
    Односвязный список.
    Храним head, (опционально) tail для O(1) append, и _size.
    """

    __slots__ = ("head", "tail", "_size")

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

        if iterable is not None:
            for v in iterable:
                self.append(v)

    def append(self, value: Any) -> None:
        """Добавить в конец за O(1) благодаря tail."""
        new_node = Node(value)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def prepend(self, value: Any) -> None:
        """Добавить в начало за O(1)."""
        new_node = Node(value, next=self.head)
        self.head = new_node
        if self.tail is None:  # список был пуст
            self.tail = new_node
        self._size += 1

    def insert(self, idx: int, value: Any) -> None:
        """
        Вставка по индексу.
        Допустимо: idx в [0, len]
        - idx == 0 -> prepend
        - idx == len -> append
        """
        if idx < 0 or idx > self._size:
            raise IndexError("index out of range")

        if idx == 0:
            self.prepend(value)
            return
        if idx == self._size:
            self.append(value)
            return

        prev = self.head
        for _ in range(idx - 1):
            assert prev is not None
            prev = prev.next

        # prev гарантированно не None, т.к. idx в допустимом диапазоне
        new_node = Node(value, next=prev.next)  # type: ignore[union-attr]
        prev.next = new_node  # type: ignore[union-attr]
        self._size += 1

    def remove(self, value: Any) -> None:
        """
        Удаляет первое вхождение value.
        Поведение как у list.remove: если нет — ValueError.
        """
        prev: Optional[Node] = None
        cur = self.head

        while cur is not None:
            if cur.value == value:
                # удаляем cur
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next

                if cur is self.tail:
                    self.tail = prev

                self._size -= 1
                if self._size == 0:
                    self.head = self.tail = None
                return

            prev, cur = cur, cur.next

        raise ValueError("value not found in list")


    def __iter__(self) -> Iterator[Any]:
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SinglyLinkedList({list(self)!r})"
```

## Результат работы


![](/images/lab10/structures.png)
![](/images/lab10/linked_list.png)
