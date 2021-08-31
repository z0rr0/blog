import timeit
from typing import Callable, Dict, List, Set, Union

import matplotlib.pyplot as plt

DataType = Union[Dict[int, str], List[int], Set[int]]


class BaseBench:

    def __init__(self, n: int = 1) -> None:
        self.n = n

    def get_new_dict(self) -> Dict[int, str]:
        raise NotImplementedError

    def get_filtered_dict(self, data: Dict[int, str]) -> Dict[int, str]:
        raise NotImplementedError

    def get_new_set(self) -> Set[int]:
        raise NotImplementedError

    def get_filtered_set(self, data: Set[int]) -> Set[int]:
        raise NotImplementedError

    def get_new_list(self) -> List[int]:
        raise NotImplementedError

    def get_filtered_list(self, data: List[int]) -> List[int]:
        raise NotImplementedError


class CycleBench(BaseBench):

    def get_new_dict(self) -> Dict[int, str]:
        result = {}
        for i in range(self.n):
            if i % 2:
                result[i] = 'odd'
            else:
                result[i] = 'even'
        return result

    def get_filtered_dict(self, data: Dict[int, str]) -> Dict[int, str]:
        result = {}
        for key, value in data.items():
            if key % 2:
                result[key] = value
        return result

    def get_new_list(self) -> List[int]:
        result = []
        for i in range(self.n):
            result.append(i * 2)
        return result

    def get_filtered_list(self, data: List[int]) -> List[int]:
        result = []
        for i in data:
            if i % 2:
                result.append(i)
        return result

    def get_new_set(self) -> Set[int]:
        result = set()
        for i in range(self.n):
            if i % 2:
                result.add(i)
        return result

    def get_filtered_set(self, data: Set[int]) -> Set[int]:
        result = set()
        for i in data:
            if i % 2:
                result.add(i)
        return result


class ComprehensionBench(BaseBench):

    def get_new_dict(self) -> Dict[int, str]:
        return {i: 'odd' if i % 2 else 'even' for i in range(self.n)}

    def get_filtered_dict(self, data: Dict[int, str]) -> Dict[int, str]:
        return {key: value for key, value in data.items() if key % 2}

    def get_new_list(self) -> List[int]:
        return [i * 2 for i in range(self.n)]

    def get_filtered_list(self, data: List[int]) -> List[int]:
        return [i for i in data if i % 2]

    def get_new_set(self) -> Set[int]:
        return {i for i in range(self.n) if i % 2}

    def get_filtered_set(self, data: Set[int]) -> Set[int]:
        return {i for i in data if i % 2}


class Tester:

    def __init__(
            self,
            cmpr: ComprehensionBench,
            cycle: CycleBench,
            sizes: List[int],
            timeit_num: int = 100) -> None:
        self.cmpr = cmpr
        self.cycle = cycle
        self.timeit_num = timeit_num
        self.sizes = sizes

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('How comprehension is faster than cycle')
        self.ax.set_xlabel('items in collection')
        self.ax.set_ylabel('seconds')

    def finalize(self, file_name: str) -> None:
        self.ax.legend()
        self.fig.savefig(file_name)
        print(f'result image was saved to {file_name}')

    def plot(self, y: List[float], label: str) -> None:
        self.ax.plot(self.sizes, y, label=label)
        print(f'added plot figure "{label}"')

    def _new(self, cycle_func: Callable[[None], DataType], cmpr_func: Callable[[None], DataType]) -> List[float]:
        result = []
        for n in self.sizes:
            self.cycle.n = self.cmpr.n = n
            time_cycle = timeit.timeit(cycle_func, number=self.timeit_num)
            time_cmpr = timeit.timeit(cmpr_func, number=self.timeit_num)
            result.append(time_cycle - time_cmpr)
        return result

    def _filtered(
            self,
            cycle_func: Callable[[DataType], DataType],
            cmpr_func: Callable[[DataType], DataType],
            data_func: Callable[[int], DataType]) -> List[float]:
        result = []
        for n in self.sizes:
            data = data_func(n)
            time_cycle = timeit.timeit(lambda: cycle_func(data), number=self.timeit_num)
            time_cmpr = timeit.timeit(lambda: cmpr_func(data), number=self.timeit_num)
            result.append(time_cycle - time_cmpr)
        return result

    def new_dict(self) -> None:
        print('run new dict creation methods')
        result = self._new(
            cycle_func=self.cycle.get_new_dict,
            cmpr_func=self.cmpr.get_new_dict,
        )
        return self.plot(result, 'new dict')

    def filtered_dict(self):
        print('run filter dict creation methods')
        result = self._filtered(
            cycle_func=self.cycle.get_filtered_dict,
            cmpr_func=self.cmpr.get_filtered_dict,
            data_func=lambda n: {i: f'value={i}' for i in range(n)},
        )
        return self.plot(result, 'dict filter')

    def new_list(self) -> None:
        print('run new list creation methods')
        result = self._new(
            cycle_func=self.cycle.get_new_list,
            cmpr_func=self.cmpr.get_new_list,
        )
        return self.plot(result, 'new list')

    def filtered_list(self):
        print('run filter list creation methods')
        result = self._filtered(
            cycle_func=self.cycle.get_filtered_list,
            cmpr_func=self.cmpr.get_filtered_list,
            data_func=lambda n: [i for i in range(n)],
        )
        return self.plot(result, 'list filter')

    def new_set(self) -> None:
        print('run new set creation methods')
        result = self._new(
            cycle_func=self.cycle.get_new_set,
            cmpr_func=self.cmpr.get_new_set,
        )
        return self.plot(result, 'new set')

    def filtered_set(self):
        print('run filter set creation methods')
        result = self._filtered(
            cycle_func=self.cycle.get_filtered_set,
            cmpr_func=self.cmpr.get_filtered_set,
            data_func=lambda n: {i for i in range(n)},
        )
        return self.plot(result, 'set filter')

    def run(self) -> None:
        self.new_dict()
        self.filtered_dict()

        self.new_list()
        self.filtered_list()

        self.new_set()
        self.filtered_set()

    def process(self, file_name: str) -> None:
        self.run()
        self.finalize(file_name)


def main() -> None:
    cycle = CycleBench()
    cmpr = ComprehensionBench()

    sizes = [10 * i for i in range(1, 101)]
    t = Tester(cmpr=cmpr, cycle=cycle, sizes=sizes)
    t.process(f'comprehension_vs_cycle_small.png')

    sizes = [10_000 * i for i in range(1, 11)]
    t = Tester(cmpr=cmpr, cycle=cycle, sizes=sizes)
    t.process(f'comprehension_vs_cycle_big.png')


if __name__ == '__main__':
    main()
