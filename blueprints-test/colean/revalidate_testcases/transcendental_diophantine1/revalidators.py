import re
from typing import List


__all__ = [
    "pow_mod_eq_zero",
    "observe_mod_cycle",
    "utilize_mod_cycle",
    "exhaust_mod_cycle",
    "compute_mod_add",
    "compute_mod_sub",
    "transcendental_diophantine1_double_enumeration",
    "transcendental_diophantine1_front_enumeration",
    "transcendental_diophantine1_back_enumeration",
]


def pow_mod_eq_zero(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # <base> ^ <ident> % <mod> = 0
    prop_pattern = re.compile(r"\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\s*=\s*0\s*")
    prop_match = prop_pattern.fullmatch(prop)
    if not prop_match: return False
    
    base, ident, mod = \
        int(prop_match.group(1)), prop_match.group(2), int(prop_match.group(3))
    if base < 2 or mod < 2: return False

    if len(verified_facts) != 2: return False
    all_facts = ", ".join(verified_facts)
    
    # <ident2> % 1 = 0, <ident3> >= <min_value>
    facts_pattern = re.compile(
        r"\s*(\w+)\s*%\s*1\s*=\s*0, \s*(\w+)\s*>=\s*(\d+)\s*"
    )
    facts_match = facts_pattern.fullmatch(all_facts)
    if not facts_match: return False
    
    ident2, ident3, min_value = \
        facts_match.group(1), facts_match.group(2), int(facts_match.group(3))
        
    if ident2 != ident or ident3 != ident or min_value < 1: return False
    
    # base, mod, min_value
    result = (((base ** min_value) % mod) == 0)
    
    if not result: return False
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"pow_mod_eq_zero: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def observe_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("observe_mod_cycle", prop, ", ".join(verified_facts)))
    
    return True


def utilize_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("utilize_mod_cycle", prop, ", ".join(verified_facts)))
    
    return True


def exhaust_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("exhaust_mod_cycle", prop, ", ".join(verified_facts)))
    
    return True


def compute_mod_add(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("compute_mod_add", prop, ", ".join(verified_facts)))
    
    return True


def compute_mod_sub(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("compute_mod_sub", prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_double_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("transcendental_diophantine1_double_enumeration", prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_front_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("transcendental_diophantine1_front_enumeration", prop, ", ".join(verified_facts)))
    
    return True


def transcendental_diophantine1_back_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    input(("transcendental_diophantine1_back_enumeration", prop, ", ".join(verified_facts)))
    
    return True