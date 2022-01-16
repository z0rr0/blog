from typing import Generator, Iterator, List


def generator(start: int, stop: int, step: int = 1) -> Generator[int, None, None]:
    """
    Генератор целых чисел от start до stop с шагом step.

    >>> list(generator(5, 13, 2))
    [5, 7, 9, 11, 13]
    """
    i = start
    while i <= stop:
        yield i
        i += step


class SquareIterator:
    """
    Генератор квадратов чисел.

    >>> s = SquareIterator([3, 5, 7])
    >>> list(s)
    [9, 25, 49]
    >>> list(s)
    []
    """

    def __init__(self, data: List[int]) -> None:
        self.index = 0
        self.total = len(data)
        self.data = data

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.index >= self.total:
            raise StopIteration
        value = self.data[self.index] ** 2
        self.index += 1
        return value


class SquareInfIterator(SquareIterator):
    """
    Генератор квадратов чисел с возможностью повторного вызова.

    >>> s = SquareIterator([3, 5, 7])
    >>> list(s)
    [9, 25, 49]
    >>> list(s)
    [9б 25 49]
    """

    def __iter__(self) -> Iterator[int]:
        self.index = 0
        return self


class RangeGenerator:
    """
    Range генератор.

    >>> r = RangeGenerator(5, 13, 2)
    >>> list(r)
    [5, 7, 9, 11, 13]
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> Generator[int, None, None]:
        i = self.start
        while i <= self.stop:
            yield i
            i += self.step


class FileLineLenGenerator:
    """
    Генератор длин строк файла.

    >>> f = FileLineLenGenerator('my_file.txt')
    >>> list(f)
    [4, 3, 8]
    """
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def __iter__(self) -> Generator[int, None, None]:
        with open(self.file_name) as f:
            for line in f:
                yield len(line)
