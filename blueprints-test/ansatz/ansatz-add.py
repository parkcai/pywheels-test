import numexpr
import numpy as np
from pywheels.blueprints.ansatz import Ansatz
from pywheels.math_funcs.integral import integral_1d_func


def main():
    
    ansatz1 = Ansatz(
        expression = "param1 * exp(param2 * x)",
        variables = ["x"],
        functions = ["exp"],
    )
    
    def numeric_ansatz_user(numeric_ansatz):
        
        f1 = lambda x: np.sin(x)
        
        f2 = lambda x: numexpr.evaluate(
            ex = numeric_ansatz,
            local_dict = {
                "x": x
            }
        )
        
        error = integral_1d_func(
            func = lambda x: np.square((f1(x) - f2(x))),
            start = 0,
            end = 2 * np.pi,
        )
        
        return error
    
    param_ranges = [(-5.0, 5.0)]
    trial_num = 10
    
    _, best_output = ansatz1.apply_to(
        numeric_ansatz_user = numeric_ansatz_user,
        param_ranges = param_ranges * ansatz1.get_param_num(),
        trial_num = trial_num,
        mode = "optimize",
        do_minimize = True,
    )
    
    print(f"拟设{ansatz1.to_expression()}的最小误差：{best_output:.4f}")
    
    ansatz2 = Ansatz(
        expression = "param1 * exp(param2 * x)",
        variables = ["x"],
        functions = ["exp"],
    )
    
    sum_ansatz = ansatz1 + ansatz2
    
    _, best_output = sum_ansatz.apply_to(
        numeric_ansatz_user = numeric_ansatz_user,
        param_ranges = param_ranges * sum_ansatz.get_param_num(),
        trial_num = trial_num,
        mode = "optimize",
        do_minimize = True,
    )
    
    print(f"拟设{sum_ansatz.to_expression()}的最小误差：{best_output:.4f}")


if __name__ == "__main__":
    
    main()
