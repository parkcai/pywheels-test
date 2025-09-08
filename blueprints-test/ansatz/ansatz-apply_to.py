from time import perf_counter
from pywheels.blueprints.ansatz import Ansatz
from pywheels.task_runner.task_runner import execute_python_script


def main():
    
    ansatz = Ansatz(
        expression = "(x - param1) ** param2 + param3",
        variables = ["x"],
        functions = [],
    )
    
    def numeric_ansatz_user(
        numeric_ansatz: str
    ):
        
        script = f"""import numpy as np


if __name__ == "__main__":

    x = 5.0
    y_truth = 0.0
    y_pred = {numeric_ansatz}
    
    mean_absolute_error = abs(y_pred - y_truth)
    
    print(mean_absolute_error, end = "")
"""

        run_script_result = execute_python_script(
            script_content = script,
            timeout_seconds = 1,
            python_command = "python",
        )

        if not run_script_result["success"]:
            return 100.0

        return float(run_script_result["stdout"])
    
    param_ranges = [
        (2.0, 4.0),
        (2.0, 4.0),
        (-0.5, 0.5),
    ]

    start = perf_counter()
    
    best_params, best_output = ansatz.apply_to(
        numeric_ansatz_user = numeric_ansatz_user,
        param_ranges = param_ranges,
        trial_num = 100,
        method = "random",
        do_minimize = True,
    )

    end = perf_counter()
    
    print(
        f"【随机搜索】在当前拟设与参数范围下，最小误差为：{best_output}\n"
        f"在参数{best_params}下取到\n"
        f"（用时 {int(end-start)} 秒）"
    )

    start = perf_counter()

    best_params, best_output = ansatz.apply_to(
        numeric_ansatz_user = numeric_ansatz_user,
        param_ranges = param_ranges,
        trial_num = 1,
        method = "L-BFGS-B",
        do_minimize = True,
    )

    end = perf_counter()
    
    print(
        f"【优化搜索】在当前拟设与参数范围下，最小误差为：{best_output}\n"
        f"在参数{best_params}下取到\n"
        f"（用时 {int(end-start)} 秒）"
    )


if __name__ == "__main__":
    
    main()
