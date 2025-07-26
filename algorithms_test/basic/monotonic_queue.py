from typing import List
from typing import TypeVar
from typing import Sequence
from typing import Callable
from typing import Protocol
from typing import runtime_checkable
from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.algorithms.basic.monotonic_queue import sliding_window_greatest
from pywheels.algorithms.basic.monotonic_queue import sliding_window_smallest


SlidingWindowBestCase = namedtuple(
    "SlidingWindowBestCase", 
    [
        "data", "window_size", "key", "best_means_greatest",
    ]
)


sliding_window_best_cases = [
        
    # 1. 整数找最大
    SlidingWindowBestCase(
        data = [1, 3, 2, 5, 4],
        window_size = 3,
        key = lambda x: x,
        best_means_greatest = True,
    ),

    # 2. 整数找最小
    SlidingWindowBestCase(
        data = [1, 3, 2, 5, 4],
        window_size = 3,
        key = lambda x: x,
        best_means_greatest = False,
    ),

    # 3. 所有元素一样
    SlidingWindowBestCase(
        data = [7] * 10,
        window_size = 4,
        key = lambda x: x,
        best_means_greatest = True,
    ),

    # 4. 负数和正数混合，找最大
    SlidingWindowBestCase(
        data = [-3, -1, 0, 2, -2, 4, -1],
        window_size = 3,
        key = lambda x: x,
        best_means_greatest = True,
    ),

    # 5. 字符串按长度找最长
    SlidingWindowBestCase(
        data = ["a", "abc", "de", "fghi", "j"],
        window_size = 2,
        key = len,
        best_means_greatest = True,
    ),

    # 6. 字符串按字母顺序找最小
    SlidingWindowBestCase(
        data = ["banana", "apple", "fig", "cherry", "date"],
        window_size = 3,
        key = lambda x: x,
        best_means_greatest = False,
    ),

    # 7. 元组按第一个元素找最大
    SlidingWindowBestCase(
        data = [(1, 'a'), (5, 'b'), (3, 'c'), (4, 'd'), (2, 'e')],
        window_size = 3,
        key = lambda x: x[0],
        best_means_greatest = True,
    ),

    # 8. 元组按第二个字母倒序找最小（反过来意思其实是按字母顺序找最大）
    SlidingWindowBestCase(
        data = [(10, 'x'), (20, 'b'), (30, 'a'), (40, 'c')],
        window_size = 2,
        key = lambda x: -ord(x[1]),
        best_means_greatest = False,
    ),

    # 9. 边界：window_size == len(data)
    SlidingWindowBestCase(
        data = [4, 7, 1, 3, 5],
        window_size = 5,
        key = lambda x: x,
        best_means_greatest = True,
    ),

    # 10. 较长数组，反复波动，测试稳定性
    SlidingWindowBestCase(
        data = [i % 7 for i in range(20)],
        window_size = 5,
        key = lambda x: x,
        best_means_greatest = False,
    ),
]


class TestSlidingWindowBest(TestCase):
    
    def test_sliding_window_best(self):
        
        for i, case in enumerate(sliding_window_best_cases):
            
            with self.subTest(i = i):
                
                if case.best_means_greatest:
                    result = sliding_window_greatest(
                        data = case.data,
                        window_size = case.window_size,
                        key = case.key,
                    )
                else:
                    result = sliding_window_smallest(
                        data = case.data,
                        window_size = case.window_size,
                        key = case.key,
                    )
                    
                expected = sliding_window_best_plain_and_trusted(
                    data = case.data,
                    window_size = case.window_size,
                    key = case.key,
                    best_means_greatest = case.best_means_greatest,
                )
                
                self.assertEqual(result, expected)
                
                
@runtime_checkable
class SupportsRichComparison(Protocol):
    def __gt__(self, other)-> bool: ...
    def __eq__(self, other)-> bool: ...
    def __lt__(self, other)-> bool: ...


DatumType = TypeVar("DatumType")
KeyType = TypeVar("KeyType", bound = SupportsRichComparison)


def sliding_window_best_plain_and_trusted(
    data: Sequence[DatumType],
    window_size: int,
    key: Callable[[DatumType], KeyType],
    best_means_greatest: bool,
)-> List[DatumType]:
    
    results = []      
      
    for i in range(len(data) - window_size + 1):
        
        best = max if best_means_greatest else min
        
        result = best(
            data[i:i+window_size],
            key = key,
        )
        
        results.append(result)

    return results


def main():
    
    unittest_main()


if __name__ == "__main__":
    
    main()