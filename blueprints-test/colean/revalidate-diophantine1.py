from typing import List
from os.path import sep as seperator
from pywheels.blueprints.colean import CoLeanRechecker


def pow_mod_eq_zero(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def observe_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def utilize_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def exhaust_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def compute_mod_add(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def compute_mod_sub(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_double_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_front_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_back_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input((prop, ", ".join(verified_facts)))
    
    return True


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
            f"revalidate-testcases{seperator}test.lean"
        ),
    )
    
    if valid:
        print("lean code 已通过复核！")
        
    else:
        
        invalid_cause = diophantine_lean_proxy.get_invalid_cause()
        
        print(f"lean code 未通过复核，原因如下：\n{invalid_cause}")


if __name__ == "__main__":
    
    main()