from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.blueprints.ansatz import Ansatz


AnsatzAddCase = namedtuple(
    "AnsatzAddCase", 
    [
        "expression1", "expression2",
        "variables", "functions",
        "expected",
    ]
)


test_ansatz_add_cases = [
    # 基本加法测试
    AnsatzAddCase(
        expression1 = "param1 * x",
        expression2 = "param1 * y",
        variables = ["x", "y"],
        functions = [],
        expected = "param1 * x + param2 * y"
    ),
    
    # 函数表达式加法
    AnsatzAddCase(
        expression1 = "sin(param1 * x)",
        expression2 = "cos(param1 * y)",
        variables = ["x", "y"],
        functions = ["sin", "cos"],
        expected = "param1 * sin(param2 * x) + param3 * cos(param4 * y)"
    ),
    
    # 复杂表达式加法
    AnsatzAddCase(
        expression1 = "param1 * x + param2 * y",
        expression2 = "param1 * sin(x) + param2 * cos(y)",
        variables = ["x", "y"],
        functions = ["sin", "cos"],
        expected = "param1 * x + param2 * y + param3 * sin(x) + param4 * cos(y)"
    ),
    
    # 参数乘法优化测试（不应重复添加参数）
    AnsatzAddCase(
        expression1 = "param1 * x",
        expression2 = "param1 * x / param2",
        variables = ["x"],
        functions = [],
        expected = "param1 * x + param2 * x / param3"
    ),
    
    # 多参数复杂表达式加法
    AnsatzAddCase(
        expression1 = "exp(param1 * x) + sin(param2 * y)",
        expression2 = "log(param1 * z) + sqrt(param2 * w)",
        variables = ["x", "y", "z", "w"],
        functions = ["exp", "sin", "log", "sqrt"],
        expected = "param1 * exp(param2 * x) + param3 * sin(param4 * y) + param5 * log(param6 * z) + param7 * sqrt(param8 * w)"
    ),
    
    # 一元操作符测试【未通过】
    AnsatzAddCase(
        expression1 = "-param1 * x",
        expression2 = "+param1 * y",
        variables = ["x", "y"],
        functions = [],
        expected = "param1 * (-x) + param2 * y"
    ),
    
    # 嵌套函数加法
    AnsatzAddCase(
        expression1 = "sin(cos(param1 * x))",
        expression2 = "exp(log(param1 * y))",
        variables = ["x", "y"],
        functions = ["sin", "cos", "exp", "log"],
        expected = "param1 * sin(cos(param2 * x)) + param3 * exp(log(param4 * y))"
    ),
    
    # 幂运算加法
    AnsatzAddCase(
        expression1 = "param1 * x ** param2",
        expression2 = "param1 * y ** param2",
        variables = ["x", "y"],
        functions = [],
        expected = "param1 * x ** param2 + param3 * y ** param4"
    ),
    
    # 除法表达式加法【未通过】
    AnsatzAddCase(
        expression1 = "param1 / x",
        expression2 = "param1 / y",
        variables = ["x", "y"],
        functions = [],
        expected = "param1 / x + param2 / y"
    ),
    
    # 混合运算符加法【未通过】
    AnsatzAddCase(
        expression1 = "param1 * x + param2 / y",
        expression2 = "param1 * sin(x) - param2 * cos(y)",
        variables = ["x", "y"],
        functions = ["sin", "cos"],
        expected = "param1 * x + param2 / y + param3 * sin(x) - param4 * cos(y)"
    ),
    
    # 复杂括号表达式加法【未通过】
    AnsatzAddCase(
        expression1 = "(param1 + param2 * x) / (y + param3)",
        expression2 = "(param1 - param2 * y) * (x + param3)",
        variables = ["x", "y"],
        functions = [],
        expected = "param1 * (param2 + param3 * x) / (y + param4) + param5 * (param6 - param7 * y) * (x + param8)"
    ),
    
    # 单变量多函数加法
    AnsatzAddCase(
        expression1 = "sin(param1 * x) + cos(param2 * x)",
        expression2 = "tan(param1 * x) + exp(param2 * x)",
        variables = ["x"],
        functions = ["sin", "cos", "tan", "exp"],
        expected = "param1 * sin(param2 * x) + param3 * cos(param4 * x) + param5 * tan(param6 * x) + param7 * exp(param8 * x)"
    ),
    
    # 参数重用测试
    AnsatzAddCase(
        expression1 = "param1 * x + param1 * y",
        expression2 = "param1 * z + param1 * w",
        variables = ["x", "y", "z", "w"],
        functions = [],
        expected = "param1 * x + param1 * y + param2 * z + param2 * w"
    ),
    
    # 复杂嵌套加法
    AnsatzAddCase(
        expression1 = "exp(sin(param1 * x) + cos(param2 * y))",
        expression2 = "log(sqrt(param1 * z) + tan(param2 * w))",
        variables = ["x", "y", "z", "w"],
        functions = ["exp", "sin", "cos", "log", "sqrt", "tan"],
        expected = "param1 * exp(sin(param2 * x) + cos(param3 * y)) + param4 * log(sqrt(param5 * z) + tan(param6 * w))"
    )
]


class TestAnsatzAdd(TestCase):
    
    def test_ansatz_add(self):
        
        for i, case in enumerate(test_ansatz_add_cases):
            
            with self.subTest(i = i):
                
                ansatz1 = Ansatz(
                    expression = case.expression1,
                    variables = case.variables,
                    functions = case.functions
                )
                
                ansatz2 = Ansatz(
                    expression = case.expression2,
                    variables = case.variables,
                    functions = case.functions
                )
                
                sum_ansatz = ansatz1 + ansatz2

                self.assertEqual(
                    sum_ansatz.to_expression(), 
                    case.expected,
                )
                
                
def main():
    
    unittest_main()


if __name__ == "__main__":
    
    main()
