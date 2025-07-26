from typing import List
from typing import Union
from typing import TypeVar
from typing import Sequence
from typing import Callable
from typing import Protocol
from typing import runtime_checkable
from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.algorithms.basic.monotonic_stack import next_greater_element
from pywheels.algorithms.basic.monotonic_stack import next_smaller_element


NextQualifiedElementCase = namedtuple(
    "NextQualifiedElementCase", 
    [
        "data", "key", "right_direction", "strict", 
        "return_index", "fill_factory", "qualified_means_greater",
    ]
)


next_qualified_element_cases = [
    
    # 1. 基础：整数，右查找，严格，找大
    NextQualifiedElementCase(
        data = [2, 1, 3],
        key = lambda x: x,
        right_direction = True,
        strict = True,
        return_index = False,
        fill_factory = lambda: -1,
        qualified_means_greater = True,
    ),

    # 2. 基础：整数，右查找，非严格，找小
    NextQualifiedElementCase(
        data = [3, 2, 2, 4],
        key = lambda x: x,
        right_direction = True,
        strict = False,
        return_index = False,
        fill_factory = lambda: -1,
        qualified_means_greater = False,
    ),

    # 3. 返回索引，严格，找小
    NextQualifiedElementCase(
        data = [5, 4, 3, 2],
        key = lambda x: x,
        right_direction = True,
        strict = True,
        return_index = True,
        fill_factory = lambda: -1,
        qualified_means_greater = False,
    ),

    # 4. key 为字符串长度
    NextQualifiedElementCase(
        data = ["a", "bbb", "cc", "dddd"],
        key = len,
        right_direction = True,
        strict = True,
        return_index = False,
        fill_factory = lambda: "",
        qualified_means_greater = True,
    ),

    # 5. key 为元组中元素，非严格，反向查找
    NextQualifiedElementCase(
        data = [(3, "c"), (2, "b"), (1, "a")],
        key = lambda x: x[0],
        right_direction = False,
        strict = False,
        return_index = False,
        fill_factory = lambda: (-1, ""),
        qualified_means_greater = False,
    ),

    # 6. 全相等元素，strict=False，右查找，找大
    NextQualifiedElementCase(
        data = [5, 5, 5],
        key = lambda x: x,
        right_direction = True,
        strict = False,
        return_index = True,
        fill_factory = lambda: -1,
        qualified_means_greater = True,
    ),

    # 7. 空栈情况无结果，strict=True，左查找
    NextQualifiedElementCase(
        data = [1, 2, 3],
        key = lambda x: x,
        right_direction = False,
        strict = True,
        return_index = False,
        fill_factory = lambda: -999,
        qualified_means_greater = False,
    ),

    # 8. fill_factory 返回非 int（return_index=True，应触发验证）
    NextQualifiedElementCase(
        data = [3, 1],
        key = lambda x: x,
        right_direction = True,
        strict = True,
        return_index = True,
        fill_factory = lambda: -1,  # 合法
        qualified_means_greater = True,
    ),

    # 9. 用自定义 key 顺序打乱
    NextQualifiedElementCase(
        data = ["apple", "banana", "fig", "cherry"],
        key = lambda x: {"apple": 3, "banana": 2, "fig": 4, "cherry": 1}[x],
        right_direction = True,
        strict = True,
        return_index = False,
        fill_factory = lambda: "",
        qualified_means_greater = True,
    ),

    # 10. 反向查找，返回索引，找大
    NextQualifiedElementCase(
        data = [3, 1, 2],
        key = lambda x: x,
        right_direction = False,
        strict = True,
        return_index = True,
        fill_factory = lambda: -1,
        qualified_means_greater = True,
    ),
    
    NextQualifiedElementCase(
        data = list(range(10, 0, -1)),  # 10→1，严格找右边更大元素，均找不到
        key = lambda x: x,
        right_direction = True,
        strict = True,
        return_index = False,
        fill_factory = lambda: -1,
        qualified_means_greater = True,
    ),

    NextQualifiedElementCase(
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
        key = lambda x: x,
        right_direction = True,
        strict = False,
        return_index = True,
        fill_factory = lambda: -1,
        qualified_means_greater = False,
    ),

    NextQualifiedElementCase(
        data = [(i, chr(97 + i % 26)) for i in range(15)],
        key = lambda x: -x[0],
        right_direction = False,
        strict = True,
        return_index = False,
        fill_factory = lambda: (-1, "?"),
        qualified_means_greater = True,
    ),

    NextQualifiedElementCase(
        data = [2] * 12,
        key = lambda x: x,
        right_direction = True,
        strict = False,
        return_index = True,
        fill_factory = lambda: -1,
        qualified_means_greater = True,
    ),

    NextQualifiedElementCase(
        data = [i ** 2 % 7 for i in range(12)],  # → [0,1,4,2,2,4,1,0,1,4,2,2]
        key = lambda x: x,
        right_direction = False,
        strict = True,
        return_index = False,
        fill_factory = lambda: -999,
        qualified_means_greater = False,
    ),
]


class TestCheckAnsatzFormat(TestCase):
    
    def test_next_qualified_element(self):
        
        for i, case in enumerate(next_qualified_element_cases):
            
            with self.subTest(i=i):
                
                if case.qualified_means_greater:
                    result = next_greater_element(
                        data = case.data,
                        key = case.key,
                        right_direction = case.right_direction,
                        strict = case.strict,
                        return_index = case.return_index,
                        fill_factory = case.fill_factory,
                    )
                else:
                    result = next_smaller_element(
                        data = case.data,
                        key = case.key,
                        right_direction = case.right_direction,
                        strict = case.strict,
                        return_index = case.return_index,
                        fill_factory = case.fill_factory,
                    )
                    
                expected = next_qualified_element_plain_and_trusted(
                    data = case.data,
                    key = case.key,
                    right_direction = case.right_direction,
                    strict = case.strict,
                    return_index = case.return_index,
                    fill_factory = case.fill_factory,
                    qualified_means_greater = case.qualified_means_greater,
                )
                
                self.assertEqual(result, expected)
                

@runtime_checkable
class SupportsRichComparison(Protocol):
    def __gt__(self, other)-> bool: ...
    def __eq__(self, other)-> bool: ...
    def __lt__(self, other)-> bool: ...


DatumType = TypeVar("DatumType")
KeyType = TypeVar("KeyType", bound = SupportsRichComparison)


def next_qualified_element_plain_and_trusted(
    data: Sequence[DatumType],
    key: Callable[[DatumType], KeyType],
    right_direction: bool,
    strict: bool,
    return_index: bool,
    fill_factory: Callable[[], Union[int, DatumType]],
    qualified_means_greater: bool,
)-> Union[List[int], List[DatumType]]:
        
    def is_qualified_for(
        datum1: DatumType, 
        datum2: DatumType,
    )-> bool:
        
        datum1_key = key(datum1)
        datum2_key = key(datum2)
        
        return (qualified_means_greater and datum2_key > datum1_key) \
            or (not qualified_means_greater and datum2_key < datum1_key) \
            or (not strict and datum2_key == datum1_key)
     
    data_length = len(data)
    results = []
    
    if right_direction:
        indices = range(data_length)
        
    else:
        indices = range(data_length - 1, -1, -1)
        
    for i in indices:
        
        qualified_datum_index = -1
        
        if right_direction:
            inner_indices = range(i + 1, data_length)
            
        else:
            inner_indices = range(i - 1, -1, -1)
        
        for j in inner_indices:
            
            if is_qualified_for(data[i], data[j]):
                qualified_datum_index = j
                break
            
        if qualified_datum_index == -1:
            result = fill_factory()
        
        else:
            
            if return_index:
                result = qualified_datum_index
                
            else:
                result = data[qualified_datum_index]
        
        results.append(result)
        
    if not right_direction: results.reverse()

    return results
            
            
def main():
    
    unittest_main()


if __name__ == "__main__":
    
    main()