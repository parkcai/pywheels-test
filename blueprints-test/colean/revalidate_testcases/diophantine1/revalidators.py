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
    "diophantine1_double_enumeration",
    "diophantine1_front_enumeration",
    "diophantine1_back_enumeration",
]


_verbose: bool = False


def _get_modular_multiplicative_cycle(base, mod):
    
    if base < 1 or mod < 2 or math.gcd(base, mod) != 1: raise ValueError
    
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


def _exhaust_diophantine1(a, b, c, x_max, y_max):
    
    if x_max is None and y_max is None: raise ValueError
    if x_max is not None and x_max < 0: raise ValueError
    if y_max is not None and y_max < 0: raise ValueError
    if a < 2 or b < 1 or c < 2: raise ValueError
    
    result = []
    
    current_a = a
    current_c = c
    current_x = 1
    current_y = 1
    
    while (x_max is not None and y_max is not None and (current_x <= x_max or current_y <= y_max)) or \
        (x_max is None and y_max is not None and current_y <= y_max) or \
        (x_max is not None and y_max is None and current_x <= x_max):
            
        if current_a + b == current_c:
            result.append((current_x, current_y))
            current_a *= a; current_x += 1
            
        elif current_a + b < current_c:
            current_a *= a; current_x += 1
            
        else:
            current_c *= c; current_y += 1
    
    return result


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
        
        if _verbose:
            print(
                f"pow_mod_eq_zero: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
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
        
        if _verbose:
            print(
                f"observe_mod_cycle: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
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
        
        if _verbose:
            print(
                f"utilize_mod_cycle: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
        return False


def exhaust_mod_cycle(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
    
        if prop != "False": return False
        
        if len(verified_facts) != 3: return False
        all_facts = ", ".join(verified_facts)
        
        # <pow> % 1 = 0, <pow2> >= 1, 
        # List.Mem (<base> ^ <pow3> % <mod>) [<value>, <value>, ..., <value>]
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0, "
            r"\s*(\w+)\s*>=\s*1\s*, "
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*"
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        _pow, _pow2, base, _pow3, mod, values_string = \
            facts_match.group(1), facts_match.group(2), int(facts_match.group(3)), \
                facts_match.group(4), int(facts_match.group(5)), facts_match.group(6)
        values = [int(s.strip()) for s in values_string.split(",") if s.strip()]
        
        if _pow2 != _pow or _pow3 != _pow: return False
        if base < 1 or mod < 2 or math.gcd(base, mod) != 1: return False
        if any([((value < 0) or (value >= mod)) for value in values]): return False
        
        _, seen = _get_modular_multiplicative_cycle(base, mod)
        
        result = all([value not in seen for value in values])
        
        if not result: return False

        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"exhaust_mod_cycle: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True

    except Exception as error:
        if _verbose: print(error)
        return False


def compute_mod_add(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
        
        # List.Mem (<c> ^ <y> % <mod>) [<value>, <value>, ..., <value>]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        if not prop_match: return False
        
        c, y, mod, values_string = \
            int(prop_match.group(1)), prop_match.group(2), \
                int(prop_match.group(3)), prop_match.group(4)
        result_values = [int(s.strip()) for s in values_string.split(",") if s.strip()]

        if len(verified_facts) != 2: return False
        all_facts = ", ".join(verified_facts)
        
        # List.Mem (<a> ^ <x> % <mod2>) [<value>, <value>, ..., <value>], 
        # a2 ^ x2 + b = c2 ^ y2
        facts_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*, "
            r"\s*(\d+)\s*\^\s*(\w+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*\^\s*(\w+)\s*",
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        a, x, mod2, values_string, a2, x2, b, c2, y2 = \
            int(facts_match.group(1)), facts_match.group(2), int(facts_match.group(3)), \
                facts_match.group(4), int(facts_match.group(5)), facts_match.group(6), \
                    int(facts_match.group(7)), int(facts_match.group(8)), facts_match.group(9)
        values = [int(s.strip()) for s in values_string.split(",") if s.strip()]
                    
        if a < 2 or b < 1 or c < 2: return False
        if a2 != a or c2 != c or mod2 != mod: return False
        if x2 != x or y2 != y: return False
        if mod < 1: return False
        
        true_result_values = [
            (value + b) % mod
            for value in values
        ]
        
        result = (set(result_values) == set(true_result_values))
        
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"compute_mod_add: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True

    except Exception as error:
        if _verbose: print(error)
        return False
    

def compute_mod_sub(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
        
        # List.Mem (<a> ^ <x> % <mod>) [<value>, <value>, ..., <value>]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        if not prop_match: return False
        
        a, x, mod, values_string = \
            int(prop_match.group(1)), prop_match.group(2), \
                int(prop_match.group(3)), prop_match.group(4)
        result_values = [int(s.strip()) for s in values_string.split(",") if s.strip()]

        if len(verified_facts) != 2: return False
        all_facts = ", ".join(verified_facts)
        
        # List.Mem (<c> ^ <y> % <mod2>) [<value>, <value>, ..., <value>], 
        # a2 ^ x2 + b = c2 ^ y2
        facts_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*, "
            r"\s*(\d+)\s*\^\s*(\w+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*\^\s*(\w+)\s*"
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        c, y, mod2, values_string, a2, x2, b, c2, y2 = \
            int(facts_match.group(1)), facts_match.group(2), int(facts_match.group(3)), \
                facts_match.group(4), int(facts_match.group(5)), facts_match.group(6), \
                    int(facts_match.group(7)), int(facts_match.group(8)), facts_match.group(9)
        values = [int(s.strip()) for s in values_string.split(",") if s.strip()]
                    
        if a < 2 or b < 1 or c < 2: return False
        if a2 != a or c2 != c or mod2 != mod: return False
        if x2 != x or y2 != y: return False
        if mod < 1: return False
        
        true_result_values = [
            (value - b) % mod
            for value in values
        ]
        
        result = (set(result_values) == set(true_result_values))
        
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"compute_mod_sub: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True

    except Exception as error:
        if _verbose: print(error)
        return False


def diophantine1_double_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
        
        if len(verified_facts) != 6: return False
        all_facts = ", ".join(verified_facts)
        
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <x> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <x2> >= 1, 
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <y> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <y2> >= 1, 
            # <a> ^ <x3> + <b> = <c> ^ <y3>
            r"\s*(\d+)\s*\^\s*(\w+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*\^\s*(\w+)\s*, "
            # Or (<x4> <= <x_max>) (<y4> <= y_max)
            r"\s*Or\s+\(\s*(\w+)\s*<=\s*(\d+)\s*\)\s+\(\s*(\w+)\s*<=\s*(\d+)\s*\)\s*"        
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        x, x2, y, y2, a, x3, b, c, y3, x4, x_max, y4, y_max = \
            facts_match.group(1), facts_match.group(2), facts_match.group(3), \
            facts_match.group(4), int(facts_match.group(5)), facts_match.group(6), \
            int(facts_match.group(7)), int(facts_match.group(8)), facts_match.group(9), \
            facts_match.group(10), int(facts_match.group(11)), facts_match.group(12), \
            int(facts_match.group(13)), 
            
        if x2 != x or x3 != x or x4 != x: return False
        if y2 != y or y3 != y or y4 != y: return False
        if a < 2 or b < 1 or c < 2: return False
        if x_max < 0 or y_max < 0: return False
        
        true_solutions = _exhaust_diophantine1(a, b, c, x_max, y_max)
    
        # List.Mem (<x5>, <y5>) [(<x_value>, <y_value>), ..., (<x_value>, <y_value>)]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\w+)\s*,\s*(\w+)\s*\)\s+\[\s*((?:\(\s*\d+\s*,\s*\d+\s*\)\s*,?\s*)+)\s*\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        
        if not prop_match:
            if prop != "False": return False
            solutions = []
            
        else:
            x5, y5, tuple_list_str = prop_match.groups()
            if x5 != x or y5 != y: return False
            
            tuple_pattern = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")
            solutions = [
                (int(m.group(1)), int(m.group(2)))
                for m in tuple_pattern.finditer(tuple_list_str)
            ]
            
        result = (set(solutions) == set(true_solutions))
        
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"diophantine1_double_enumeration: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
        return False


def diophantine1_front_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
        
        if len(verified_facts) != 6: return False
        all_facts = ", ".join(verified_facts)
        
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <x> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <x2> >= 1, 
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <y> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <y2> >= 1, 
            # <a> ^ <x3> + <b> = <c> ^ <y3>
            r"\s*(\d+)\s*\^\s*(\w+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*\^\s*(\w+)\s*, "
            # <x4> <= <x_max>
            r"\s*(\w+)\s*<=\s*(\d+)\s*"        
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        x, x2, y, y2, a, x3, b, c, y3, x4, x_max = \
            facts_match.group(1), facts_match.group(2), facts_match.group(3), \
            facts_match.group(4), int(facts_match.group(5)), facts_match.group(6), \
            int(facts_match.group(7)), int(facts_match.group(8)), facts_match.group(9), \
            facts_match.group(10), int(facts_match.group(11))
            
        if x2 != x or x3 != x or x4 != x: return False
        if y2 != y or y3 != y : return False
        if a < 2 or b < 1 or c < 2: return False
        if x_max < 0: return False
        
        true_solutions = _exhaust_diophantine1(a, b, c, x_max, None)
    
        # List.Mem (<x5>, <y5>) [(<x_value>, <y_value>), ..., (<x_value>, <y_value>)]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\w+)\s*,\s*(\w+)\s*\)\s+\[\s*((?:\(\s*\d+\s*,\s*\d+\s*\)\s*,?\s*)+)\s*\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        
        if not prop_match:
            if prop != "False": return False
            solutions = []
            
        else:
            x5, y5, tuple_list_str = prop_match.groups()
            if x5 != x or y5 != y: return False
            
            tuple_pattern = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")
            solutions = [
                (int(m.group(1)), int(m.group(2)))
                for m in tuple_pattern.finditer(tuple_list_str)
            ]
            
        result = (set(solutions) == set(true_solutions))
        
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"diophantine1_front_enumeration: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
        return False


def diophantine1_back_enumeration(
    prop: str,
    verified_facts: List[str],
)-> bool:
    
    try:
        
        if len(verified_facts) != 6: return False
        all_facts = ", ".join(verified_facts)
        
        facts_pattern = re.compile(
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <x> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <x2> >= 1, 
            r"\s*(\w+)\s*%\s*1\s*=\s*0\s*, " # <y> % 1 = 0,
            r"\s*(\w+)\s*>=\s*1\s*, "        # <y2> >= 1, 
            # <a> ^ <x3> + <b> = <c> ^ <y3>
            r"\s*(\d+)\s*\^\s*(\w+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*\^\s*(\w+)\s*, "
            # <y4> <= <y_max>
            r"\s*(\w+)\s*<=\s*(\d+)\s*"        
        )
        facts_match = facts_pattern.fullmatch(all_facts)
        if not facts_match: return False
        
        x, x2, y, y2, a, x3, b, c, y3, y4, y_max = \
            facts_match.group(1), facts_match.group(2), facts_match.group(3), \
            facts_match.group(4), int(facts_match.group(5)), facts_match.group(6), \
            int(facts_match.group(7)), int(facts_match.group(8)), facts_match.group(9), \
            facts_match.group(10), int(facts_match.group(11))
            
        if x2 != x or x3 != x: return False
        if y2 != y or y3 != y or y4 != y: return False
        if a < 2 or b < 1 or c < 2: return False
        if y_max < 0: return False

        true_solutions = _exhaust_diophantine1(a, b, c, None, y_max)

        # List.Mem (<x5>, <y5>) [(<x_value>, <y_value>), ..., (<x_value>, <y_value>)]
        prop_pattern = re.compile(
            r"\s*List.Mem\s+\(\s*(\w+)\s*,\s*(\w+)\s*\)\s+\[\s*((?:\(\s*\d+\s*,\s*\d+\s*\)\s*,?\s*)+)\s*\]\s*"
        )
        prop_match = prop_pattern.fullmatch(prop)
        
        if not prop_match:
            if prop != "False": return False
            solutions = []
            
        else:
            
            x5, y5, tuple_list_str = prop_match.groups()
            if x5 != x or y5 != y: return False
            tuple_pattern = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")
            solutions = [
                (int(m.group(1)), int(m.group(2)))
                for m in tuple_pattern.finditer(tuple_list_str)
            ]
            
        result = (set(solutions) == set(true_solutions))
        
        if not result: return False
        
        lined_facts = "\n".join(verified_facts)
        
        if _verbose:
            print(
                f"diophantine1_back_enumeration: prop {prop} has been revalidated "
                f"by the following verified facts:\n{lined_facts}"
            )
        
        return True
    
    except Exception as error:
        if _verbose: print(error)
        return False
    

