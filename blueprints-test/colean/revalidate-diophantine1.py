from os.path import sep as seperator
from pywheels.blueprints.colean import CoLeanRechecker
from .revalidate_testcases.diophantine1.revalidators import *


def main():
    
    diophantine_lean_proxy = CoLeanRechecker(
        claim_keyword = "Claim",
        prop_field = "prop",
    )
    
    diophantine_lean_proxy.add_revalidators(
        revalidators = [
            ("pow_mod_eq_zero", pow_mod_eq_zero),
            ("observe_mod_cycle", observe_mod_cycle),
            ("utilize_mod_cycle", utilize_mod_cycle),
            ("exhaust_mod_cycle", exhaust_mod_cycle),
            ("compute_mod_add", compute_mod_add),
            ("compute_mod_sub", compute_mod_sub),
            ("diophantine1_double_enumeration", diophantine1_double_enumeration),
            ("diophantine1_front_enumeration", diophantine1_front_enumeration),
            ("diophantine1_back_enumeration", diophantine1_back_enumeration),
        ]
    )
    
    valid = diophantine_lean_proxy.revalidate(
        lean_code = (
            f"blueprints-test{seperator}colean{seperator}"
            f"revalidate_testcases{seperator}diophantine1{seperator}transcendental_diophantine1.lean"
        ),
    )
    
    if valid:
        print("lean code 已通过复核！")
        
    else:
        
        invalid_cause = diophantine_lean_proxy.get_invalid_cause()
        
        print(f"lean code 未通过复核，原因如下：\n{invalid_cause}")


if __name__ == "__main__":
    
    main()