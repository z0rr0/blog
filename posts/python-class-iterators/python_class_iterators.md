# Классы-итераторы и генераторы в Python #blog

В языке программирования Python есть понятия [итераторов](https://docs.python.org/3/glossary.html#term-iterator) и [генераторов](https://docs.python.org/3/glossary.html#term-generator-iterator). Оба термина не очень сложные и часто является обычными вопросами для собеседований разработчиков. Но в данной статье хочется разобрать немного примеров как создавать подобные объекты с помощью классов, так как это достаточно мощный и удобный механизм.

## Итераторы и генераторы

В определении на сайте [doc.python.org](https://docs.python.org/3/glossary.html#term-iterator) говорится, что объект-итератор должен

- Содержать метод `__next__()`, вызываем встроенным методом `next()` для возвращения следующего элемента коллекции.
- Если данных больше нет, то должно возникать исключение `StopIteration`.
- Также обязателен метод `__iter__()` для возвращения объекта-итератора.

Примеры встроенных типов, примеров итераторов это `list`, `tuple`.

С генераторами тоже все довольно просто. Это объекты, возвращающие функцию генерации с выражением `yield`. Её особенность в том, что при следующем вызове, функция продолжает свою работу не с самого начала, а с места использования этого служебного слова.

```python
from typing import Generator
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
``` 

Особенно хочется подчеркнуть, что существуют удобные [выражения-генераторы](https://docs.python.org/3/glossary.html#term-generator-expression), когда отдельная функция не нужна.

## Классы

Посмотрим на примеры классов, которые являются итераторами. Например в стандартной библиотеке есть пакет `csv`, создав объект [reader](https://docs.python.org/3/library/csv.html?highlight=csv#csv.reader), можно итерироваться непосредственно по нему:

```python
import csv
csv_file = open('my_file.csv')
my_reader = csv.reader(csv_file)
for row in my_reader:
    print(row)
```

Кроме того в данном примере файл не парсится весь сразу, а данные возвращаются по ходу его чтения. Это уже поведения генератора.

Попытается написать класс с похожим поведением.

### Простой генератор

Пример класса, который может выступать генератором, возвращающим квадраты чисел из входного списка.

```python
class SquareIterator:
    """
    R квадратов чисел.
    
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
```

Но иногда хочется иметь возможность итерироваться по коллекции несколько раз, как например мы можем это делать по типу `list`. Для этого нужно дополнить метод `__iter__` сбросом начального состояния.

```python
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
```

### Произвольный генератор

Метод `__iter__` не обязан всегда возвращать `self`. В качестве возвращаемого значения ожидается любой генератор, который потом можно использовать в качестве аргумента для `next()`:

```python
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
```

Аналогичным образом можно написать генератор, похожий на `csv.reader`, когда не нужно читать файл целиком и нам интересны операции на отдельными строками:

```python
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
```

## Заключение

Python итераторы это очень мощный инструмент языка. С помощью генераторов можно совершать "ленивые" вычисления, экономив на памяти. А возможность создавать произвольные классы итераторы делает программирование более гибким.
