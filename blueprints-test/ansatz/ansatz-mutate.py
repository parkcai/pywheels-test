from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.blueprints.ansatz import Ansatz


AnsatzMutateCase = namedtuple(
    "AnsatzMutateCase", 
    [
        "expression", 
        "variables", 
        "functions",
        "seed",
        "expected",
    ]
)


test_ansatz_mutate_cases = [
    
    AnsatzMutateCase(
        expression = "sin(param1 * x) + cos(param2 * x)",
        variables = ["x"],
        functions = ["sin", "cos", "log", "exp"],
        seed = 123,
        expected = "cos(param1 * x) + log(param2 * x)",
    ),

    AnsatzMutateCase(
        expression = "log(param1 * x) * sin(param2 * x)",
        variables = ["x"],
        functions = ["sin", "cos", "log"],
        seed = 1,
        expected = "sin(param1 * x) * cos(param2 * x)",
    ),
]


class TestAnsatzMutate(TestCase):
    
    def test_ansatz_add(self):
        
        for i, case in enumerate(test_ansatz_mutate_cases):
            
            with self.subTest(i = i):
                
                ansatz = Ansatz(
                    expression = case.expression,
                    variables = case.variables,
                    functions = case.functions,
                    seed = case.seed,
                )
                
                ansatz.mutate()

                self.assertEqual(
                    ansatz.to_expression(), 
                    case.expected,
                )
                
                
def main():
    
    unittest_main()


if __name__ == "__main__":
    
    main()
