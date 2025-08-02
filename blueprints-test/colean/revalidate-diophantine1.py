from os.path import sep as seperator
from pywheels.blueprints.colean import CoLeanRechecker
from .revalidate_testcases.transcendental_diophantine1.revalidators import *


def main():
    
    diophantine_lean_proxy = CoLeanRechecker()
    
    diophantine_lean_proxy.add_revalidators(
        revalidators = [
            ("pow_mod_eq_zero", pow_mod_eq_zero),
            ("observe_mod_cycle", observe_mod_cycle),
            ("utilize_mod_cycle", utilize_mod_cycle),
            ("exhaust_mod_cycle", exhaust_mod_cycle),
            ("compute_mod_add", compute_mod_add),
            ("compute_mod_sub", compute_mod_sub),
            ("transcendental_diophantine1_double_enumeration", transcendental_diophantine1_double_enumeration),
            ("transcendental_diophantine1_front_enumeration", transcendental_diophantine1_front_enumeration),
            ("transcendental_diophantine1_back_enumeration", transcendental_diophantine1_back_enumeration),
        ]
    )
    
    valid = diophantine_lean_proxy.revalidate(
        lean_code = (
            f"blueprints-test{seperator}colean{seperator}"
            f"revalidate_testcases{seperator}transcendental_diophantine1{seperator}lean_code.lean"
        ),
    )
    
    if valid:
        print("lean code 已通过复核！")
        
    else:
        
        invalid_cause = diophantine_lean_proxy.get_invalid_cause()
        
        print(f"lean code 未通过复核，原因如下：\n{invalid_cause}")


if __name__ == "__main__":
    
    main()