import io
import contextlib
import traceback
from typing import Dict, Any
from pywheels.asker import get_string_input
from pywheels.llm_tools.get_answer import get_answer


def _run_python(
    code: str,
    verbose: bool = True,
)-> str:

    exec_scope: Dict[str, Any] = {}
    stdout_capture = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, exec_scope, exec_scope) 
        output = stdout_capture.getvalue()
        if not output:
            output = "代码已执行，但没有产生 stdout 输出。请使用 print() 来返回结果。"
            if verbose: print(f"模型进行了一次工具调用！\n尝试运行的代码：\n{code}\n工具调用结果：\n{output}")
            return output
        if verbose: print(f"模型进行了一次工具调用！\n尝试运行的代码：\n{code}\n工具调用结果：\n{output}")
        return output
    except Exception as error:
        output = f"代码执行失败: {error}\n调用栈：\n{traceback.format_exc()}"
        if verbose: print(f"模型进行了一次工具调用！\n尝试运行的代码：\n{code}\n工具调用结果：\n{output}")
        return output


python_tool = {
    "name": "execute_python_code",
    "description": (
        "执行一个 Python 代码块并返回其 stdout 输出。"
        "用于需要数值计算、解方程或调用库（如 scipy, numpy）的复杂数学问题。"
        "你必须使用 `print()` 语句来返回最终的数值结果。"
    ),
    "parameters": {
        "code": {
            "type": "string",
            "description": (
                "要执行的 Python 代码字符串。"
                "例如: 'import numpy as np; print(np.pi)'"
            ),
            "required": True,
        },
    },
    "implementation": _run_python,
}


def main():
    
    model = get_string_input("请输入要使用的模型：", "GPT-5")
    prompt = (
        "请求出 zeta(x_0) 的数值，放在 \\boxed{} 中，四舍五入，保留到小数点后 5 位；"
        "其中，x_0 是方程 x = 3 sin x 的最小正根，"
        "zeta 是黎曼 ζ 函数：zeta(s) = 1 + 1/(2^s) + 1/(3^s) + ..."
    )
    print(f"[User]\n{prompt}\n")
    system_prompt = (
        "You are a helpful assistant. "
        "You must use the `execute_python_code` tool to solve complex math problems. "
        "You need to import necessary libraries like `scipy.optimize` for solving "
        "equations and `scipy.special` for zeta functions."
    )
    tools = [python_tool]
    response = get_answer(
        prompt = prompt,
        model = model,
        system_prompt = system_prompt,
        tools = tools,
    )
    print(f"[{model}]\n{response}")


if __name__ == "__main__":
    
    main()