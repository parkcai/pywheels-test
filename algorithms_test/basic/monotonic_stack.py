from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.algorithms.basic import next_greater_element
from pywheels.algorithms.basic import next_smaller_element


NextQualifiedElementCase = namedtuple(
    "NextQualifiedElementCase", 
    [
        "data", "key", "right_direction", "strict", 
        "return_index", "fill_factory", "qualified_means_greater",
        "expected",
    ]
)


next_qualified_element_cases = [
    
]


class TestCheckAnsatzFormat(TestCase):
    
    def test_next_qualified_element(self):
        
        for i, case in enumerate(next_qualified_element_cases):
            
            with self.subTest(i=i):
                
                try:
                    
                    
                
                    pass
                    
                except RuntimeError as _:
                    
                    pass
                    
                self.assertEqual(
                    ...
                )


def main():
    
    unittest_main()


if __name__ == "__main__":
    
    main()