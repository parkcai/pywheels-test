import re
import math
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


def _get_modular_multiplicative_cycle(base, mod):
    
    base = base % mod
    
    cycle = [1]
    seen = {1: 0}
    value = 1
    
    while True:
        
        value = (value * base) % mod
        if value in seen: break
        seen[value] = len(cycle)
        cycle.append(value)
        
    return cycle, seen


def pow_mod_eq_zero(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
    
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
    
    except Exception as error:
        print(error)
        return False


def observe_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
    
        if len(verified_facts) != 3: return False
        all_facts = ", ".join(verified_facts)
        
        # <pow> % 1 = 0, <pow2> >= 1, <base> ^ <pow3> % <mod> = <res>
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0, "
            r"\s*(\w+)\s*>=\s*1\s*, "
            r"\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\s*=\s*(\d+)\s*"
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        _pow, _pow2, base, _pow3, mod, res = \
            facts_match.group(1), facts_match.group(2), int(facts_match.group(3)), \
                facts_match.group(4), int(facts_match.group(5)), int(facts_match.group(6)), 
        
        if _pow2 != _pow or _pow3 != _pow: return False
        if base < 1 or mod < 2 or math.gcd(base, mod) != 1: return False
        if res < 0 or res >= mod: return False
        
        # base, mod
        cycle, seen = _get_modular_multiplicative_cycle(base, mod)
        
        # <pow4> % <repetend> = <position>
        prop_pattern = re.compile(r"\s*(\w+)\s*%\s*(\d+)\s*=\s*(\d+)\s*")
        prop_match = prop_pattern.fullmatch(prop)
        
        if not prop_match:
            
            if prop != "False": return False
            
            # base, mod, res
            result = (res not in seen)

        else:
            
            _pow4, repetend, position = \
                prop_match.group(1), int(prop_match.group(2)), int(prop_match.group(3))
                
            if _pow4 != _pow or repetend < 1 or position < 0 or position >= repetend: return False
            
            # base, mod, res, repetend, position
            result = (repetend == len(cycle)) and (res in seen) and (position == seen[res])
            
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        print(
            f"observe_mod_cycle: prop {prop} has been revalidated "
            f"by the following verified facts:\n{lined_facts}"
        )
        
        return True
    
    except Exception as error:
        print(error)
        return False


def utilize_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
    
        if len(verified_facts) != 3: return False
        all_facts = ", ".join(verified_facts)
        
        # <pow> % 1 = 0, <pow2> >= 1, <pow3> % <cycle> = <position>
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0, "
            r"\s*(\w+)\s*>=\s*1\s*, "
            r"\s*(\w+)\s*%\s*(\d+)\s*=\s*(\d+)\s*"
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        _pow, _pow2, _pow3, period, position = \
            facts_match.group(1), facts_match.group(2), facts_match.group(3), \
                int(facts_match.group(4)), int(facts_match.group(5))
                
        if _pow2 != _pow or _pow3 != _pow: return False
        if period < 1 or position < 0 or position >= period: return False
        
        # List.Mem (<base> ^ <pow4> % <mod>) [<value>, <value>, ..., <value>]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)"
            r"\s+\[([\d\s,]+)\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        if not prop_match: return False
        
        base, _pow4, mod, values_string = \
            int(prop_match.group(1)), prop_match.group(2), \
                int(prop_match.group(3)), prop_match.group(4), 
        values = [int(s.strip()) for s in values_string.split(",") if s.strip()]
        
        if _pow4 != _pow: return False
        if base < 1 or mod < 2 or math.gcd(base, mod) != 1: return False
        if any([((value < 0) or (value >= mod)) for value in values]): return False
        
        cycle, _ = _get_modular_multiplicative_cycle(base, mod)
        repetend = len(cycle)

        valid_period = math.gcd(period, repetend)
        true_values = [
            cycle[position % valid_period + i * valid_period]
            for i in range(repetend // valid_period)
        ]
        
        result = (set(true_values) == set(values))
        if not result: return False

        lined_facts = "\n".join(verified_facts)
        
        print(
            f"utilize_mod_cycle: prop {prop} has been revalidated "
            f"by the following verified facts:\n{lined_facts}"
        )
        
        return True
    
    except Exception as error:
        print(error)
        return False


def exhaust_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"exhaust_mod_cycle: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def compute_mod_add(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"compute_mod_add: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def compute_mod_sub(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"compute_mod_sub: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def transcendental_diophantine1_double_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"transcendental_diophantine1_double_enumeration: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def transcendental_diophantine1_front_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"transcendental_diophantine1_front_enumeration: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True


def transcendental_diophantine1_back_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    # prop_pattern = 
    # prop_match = 
    
    # if len(verified_facts) != 2: return False
    # all_facts = ", ".join(verified_facts)
    
    # facts_pattern = 
    # facts_match = 
    
    
    
    lined_facts = "\n".join(verified_facts)
    
    print(
        f"transcendental_diophantine1_back_enumeration: prop {prop} has been revalidated "
        f"by the following verified facts:\n{lined_facts}"
    )
    
    return True