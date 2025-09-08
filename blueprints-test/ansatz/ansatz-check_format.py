from collections import namedtuple
from unittest import TestCase
from unittest import main as unittest_main
from pywheels.blueprints.ansatz import Ansatz
        

CheckFormatCase = namedtuple(
    "CheckFormatCase", 
    ["expression", "variables", "functions", "expected", "constant_whitelist"]
)


check_format_testcases = [
    
    # ✅ 合法的复杂表达式
    CheckFormatCase(
        expression = "param1 * x + sin(param2) - param3 / (y + param4) + cos(z)",
        variables = ["x", "y", "z"],
        functions = ["sin", "cos"],
        expected = 4,
        constant_whitelist = [],
    ),
    
    # ✅ 合法的复杂表达式
    CheckFormatCase(
        expression = "-param1 * x + +param2 - sin(param3 + param4 * y)",
        variables = ["x", "y"],
        functions = ["sin"],
        expected = 4,
        constant_whitelist = [],
    ),
    
    # ✅ 合法的复杂表达式
    CheckFormatCase(
        expression = "log(param1) + sqrt(param2) + param3**x",
        variables = ["x"],
        functions = ["log", "sqrt"],
        expected = 3,
        constant_whitelist = [],
    ),
    
    # ✅ 合法的复杂表达式
    CheckFormatCase(
        expression = "abs(param1 - param2) + exp(-param3 * x)",
        variables = ["x"],
        functions = ["abs", "exp"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ❌ 错误的参数编号（跳号）
    CheckFormatCase(
        expression = "param1 + param3",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 使用常数
    CheckFormatCase(
        expression = "param1 * 2",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 使用未列出的变量
    CheckFormatCase(
        expression = "param1 * x + y",
        variables = ["x"],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 使用未列出的函数
    CheckFormatCase(
        expression = "param1 * x + tan(param2)",
        variables = ["x"],
        functions = ["sin", "cos"],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 使用非法字符
    CheckFormatCase(
        expression = "param1 * x + y$",
        variables = ["x", "y"],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 使用模块前缀的函数名
    CheckFormatCase(
        expression = "np.sin(param1) + param2",
        variables = [],
        functions = ["sin"],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法的一元运算符组合
    CheckFormatCase(
        expression = "-param1 + +param2 * x",
        variables = ["x"],
        functions = [],
        expected = 2,
        constant_whitelist = [],
    ),

    # ✅ 合法的函数嵌套
    CheckFormatCase(
        expression = "sin(cos(param1)) + log(sqrt(param2))",
        variables = [],
        functions = ["sin", "cos", "log", "sqrt"],
        expected = 2,
        constant_whitelist = [],
    ),

    # ❌ param编号不是从1开始
    CheckFormatCase(
        expression = "param0 + param1",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ param编号重复
    CheckFormatCase(
        expression = "param1 + param1 + param2",
        variables = [],
        functions = [],
        expected = 2,
        constant_whitelist = [],
    ),

    # ✅ 单变量、单函数、单参数
    CheckFormatCase(
        expression = "sin(param1 * x)",
        variables = ["x"],
        functions = ["sin"],
        expected = 1,
        constant_whitelist = [],
    ),

    # ❌ 空表达式
    CheckFormatCase(
        expression = "",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 嵌套括号与操作符混用
    CheckFormatCase(
        expression = "((param1 + param2) * x) / (y + param3) - sin(param4)",
        variables = ["x", "y"],
        functions = ["sin"],
        expected = 4,
        constant_whitelist = [],
    ),
    
    # ✅ 合法：带多个变量和嵌套函数
    CheckFormatCase(
        expression = "exp(param1 * x) + sin(param2 * y) + cos(param3 * z)",
        variables = ["x", "y", "z"],
        functions = ["exp", "sin", "cos"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ❌ 非法：出现小数点
    CheckFormatCase(
        expression = "param1 * 3.14 + x",
        variables = ["x"],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：仅使用一元运算符
    CheckFormatCase(
        expression = "-param1 + +param2",
        variables = [],
        functions = [],
        expected = 2,
        constant_whitelist = [],
    ),

    # ❌ 非法：使用双下划线（不影响合法性字符，但可作为边界测试）
    CheckFormatCase(
        expression = "param1__ + param2",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：函数嵌套，复杂组合
    CheckFormatCase(
        expression = "log(exp(sin(param1))) + param2 * x - param3 / y",
        variables = ["x", "y"],
        functions = ["log", "exp", "sin"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ❌ 非法：非法字符 @
    CheckFormatCase(
        expression = "param1 @ x",
        variables = ["x"],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 非法：函数名为非法标识符
    CheckFormatCase(
        expression = "cos(param1) + x",
        variables = ["x"],
        functions = ["cosine"],  # 未包含 'cos'
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：变量、函数、参数混合使用
    CheckFormatCase(
        expression = "sin(x) + param1 * cos(y) + param2",
        variables = ["x", "y"],
        functions = ["sin", "cos"],
        expected = 2,
        constant_whitelist = [],
    ),

    # ✅ 合法：变量名为长名字，函数混合使用
    CheckFormatCase(
        expression = "sin(long_variable_name) + param1 + param2 * cos(another_var)",
        variables = ["long_variable_name", "another_var"],
        functions = ["sin", "cos"],
        expected = 2,
        constant_whitelist = [],
    ),

    # ❌ 非法：param编号不从1开始
    CheckFormatCase(
        expression = "param2 + param3 + param4",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 非法：param编号缺失（param1, param2, param4）
    CheckFormatCase(
        expression = "param1 + param2 + param4",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：大量连续 param
    CheckFormatCase(
        expression = "param1 + param2 + param3 + param4 + param5 + param6",
        variables = [],
        functions = [],
        expected = 6,
        constant_whitelist = [],
    ),
    
    # ✅ 合法：多变量函数 + 嵌套表达式
    CheckFormatCase(
        expression = "pow(param1 + param2, param3 + param4) + x * y - param5",
        variables = ["x", "y"],
        functions = ["pow"],
        expected = 5,
        constant_whitelist = [],
    ),

    # ✅ 合法：三层函数嵌套与多变量混用
    CheckFormatCase(
        expression = "log(sqrt(abs(param1 + x))) + param2 * y - param3 / z",
        variables = ["x", "y", "z"],
        functions = ["log", "sqrt", "abs"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ❌ 非法：函数使用未注册名（pow未列出）
    CheckFormatCase(
        expression = "pow(param1, param2) + param3",
        variables = [],
        functions = ["exp", "log"],
        expected = -1,
        constant_whitelist = [],
    ),

    # ❌ 非法：函数中嵌套非法字符
    CheckFormatCase(
        expression = "log(sqrt(param1 + 3.14))",
        variables = [],
        functions = ["log", "sqrt"],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：复杂括号与多层组合
    CheckFormatCase(
        expression = "(((param1 + param2))) * ((x + y)) - cos(param3) + sin(z)",
        variables = ["x", "y", "z"],
        functions = ["cos", "sin"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ❌ 非法：param编号重复 + 未列函数
    CheckFormatCase(
        expression = "tan(param1 + param1) + param2",
        variables = [],
        functions = ["sin"],
        expected = -1,
        constant_whitelist = [],
    ),

    # ✅ 合法：三元组合函数 + 复杂操作
    CheckFormatCase(
        expression = "log(abs(sin(param1) + cos(param2))) * param3 + sqrt(param4)",
        variables = [],
        functions = ["log", "abs", "sin", "cos", "sqrt"],
        expected = 4,
        constant_whitelist = [],
    ),

    # ✅ 合法：变量 + param 混写， param 乱序
    CheckFormatCase(
        expression = "x * param1 + y * param3 + sin(param2)",
        variables = ["x", "y"],
        functions = ["sin"],
        expected = 3,
        constant_whitelist = [],
    ),

    # ✅ 合法：复合嵌套，三变量三函数
    CheckFormatCase(
        expression = "exp(sin(x) + cos(y)) + log(param1 + param2 * z)",
        variables = ["x", "y", "z"],
        functions = ["exp", "sin", "cos", "log"],
        expected = 2,
        constant_whitelist = [],
    ),

    # ❌ 非法：param后缀带下划线
    CheckFormatCase(
        expression = "param1_ + param2",
        variables = [],
        functions = [],
        expected = -1,
        constant_whitelist = [],
    ),
    
    # ✅ 合法
    CheckFormatCase(
        expression = "power(param1 + x, param2) * param3 + sqrt(log(exp(param4 + x)))",
        variables = ["x"],
        functions = ["power", "sqrt", "log", "exp"],
        expected = 4,
        constant_whitelist = [],
    ),
    
    # ❌ 非法
    CheckFormatCase(
        expression = "power(param1 + x, param2) * param3 + sqrt(log(exp(param4 + x))) + x // param5",
        variables = ["x"],
        functions = ["power", "sqrt", "log", "exp"],
        expected = -1,
        constant_whitelist = [],
    ),
    
    # ❌ 非法
    CheckFormatCase(
        expression = "power(param1 + x, param2) * param3 + sqrt(log(exp(param4 + x))) + 1",
        variables = ["x"],
        functions = ["power", "sqrt", "log", "exp"],
        expected = -1,
        constant_whitelist = [],
    ),
    
    # ✅ 合法：使用常量白名单中的数字常量
    CheckFormatCase(
        expression = "x * param1 + 0.5 * param2 + 2 * y",
        variables = ["x", "y"],
        functions = [],
        constant_whitelist = ["0.5", "2"],
        expected = 2,
    ),

    # ✅ 合法：使用常量白名单中的标识符常量
    CheckFormatCase(
        expression = "param1 * sin(pi * x) + param2 * cos(2 * pi * y)",
        variables = ["x", "y"],
        functions = ["sin", "cos"],
        constant_whitelist = ["pi", "2"],
        expected = 2,
    ),

    # ✅ 合法：混合使用变量、函数、参数和多种常量
    CheckFormatCase(
        expression = "e * param1 * x + param2 * log(2) + sqrt(pi * y)",
        variables = ["x", "y"],
        functions = ["log", "sqrt"],
        constant_whitelist = ["e", "pi", "2"],
        expected = 2,
    ),

    # ✅ 合法：常量白名单包含多种数字格式
    CheckFormatCase(
        expression = "param1 * x + 0.5 * param2 * y + 3.14 * param3 * z",
        variables = ["x", "y", "z"],
        functions = [],
        constant_whitelist = ["0.5", "3.14", "1", "100"],
        expected = 3,
    ),

    # ❌ 非法：使用未在白名单中的数字常量
    CheckFormatCase(
        expression = "x * param1 + 0.5 * param2",
        variables = ["x"],
        functions = [],
        constant_whitelist = ["1", "2"],  # 0.5 不在白名单中
        expected = -1,
    ),

    # ❌ 非法：使用未在白名单中的标识符常量
    CheckFormatCase(
        expression = "param1 * x + pi * param2",
        variables = ["x"],
        functions = [],
        constant_whitelist = ["e", "2.718"],  # pi 不在白名单中
        expected = -1,
    ),

    # ✅ 合法：空常量白名单，不允许任何常量
    CheckFormatCase(
        expression = "param1 * x + param2 * y",
        variables = ["x", "y"],
        functions = [],
        constant_whitelist = [],  # 不允许任何常量
        expected = 2,
    ),

    # ❌ 非法：空常量白名单但表达式中包含数字
    CheckFormatCase(
        expression = "param1 * x + 1 * param2 * y",
        variables = ["x", "y"],
        functions = [],
        constant_whitelist = [],  # 不允许任何常量
        expected = -1,
    ),

    # ✅ 合法：科学计数法格式的常量（如果支持）
    CheckFormatCase(
        expression = "param1 * x + 1e-5 * param2 * y",
        variables = ["x", "y"],
        functions = [],
        constant_whitelist = ["1e-5", "0.00001"],
        expected = 2,
    ),

    # ❌ 非法：科学计数法常量不在白名单中
    CheckFormatCase(
        expression = "param1 * x + 1e-5 * param2 * y",
        variables = ["x", "y"],
        functions = [],
        constant_whitelist = ["1e-6", "0.000001"],  # 1e-5 不在白名单中
        expected = -1,
    ),

    # ✅ 合法：常量与函数参数混合使用
    CheckFormatCase(
        expression = "max(param1, 0.5) + min(param2, 1.0) * x",
        variables = ["x"],
        functions = ["max", "min"],
        constant_whitelist = ["0.5", "1.0"],
        expected = 2,
    ),
    
    # ✅ 合法：拟设不含参数，param_num = 0
    CheckFormatCase(
        expression = "x + max(0.5, 1.0)",
        variables = ["x"],
        functions = ["max", "min"],
        constant_whitelist = ["0.5", "1.0"],
        expected = 0,
    )
]


class TestCheckAnsatzFormat(TestCase):
    
    def test_check_ansatz_format(self):
        
        for i, case in enumerate(check_format_testcases):
            
            with self.subTest(
                i = i, 
                expr = case.expression
            ):
                
                x = ""
                
                try:
                
                    ansatz = Ansatz(
                        expression = case.expression,
                        variables = case.variables,
                        functions = case.functions,
                        constant_whitelist = case.constant_whitelist,
                    )
                    
                    result = ansatz.get_param_num()
                    
                except RuntimeError as error:
                    
                    result = -1
                    x = error

                self.assertEqual(
                    first = result, 
                    second = case.expected, 
                    msg = (
                        f"用例 {i} 失败: {case.expression}"
                        f"{x}"
                    ),
                )
                
                
def main():

    unittest_main()


if __name__ == "__main__":
    
    main()
