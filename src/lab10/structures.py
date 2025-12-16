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