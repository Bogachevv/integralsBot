import math
import logger


def priority(s: str) -> int:
    match s:
        case ')':
            return 0
        case '+' | '-':
            return 1
        case '*' | '/':
            return 2
        case '^':
            return 3
        case "ln" | "sin" | "cos" | "tg" | "ctg" | "exp" | "sqrt":
            return 4


def is_operator(s: str) -> bool:
    return s in ["+", "-", "*", "/", "ln", "sin", "cos", "tg", "ctg", "exp", "sqrt", "^"]


def calc_operation(op, left, right):
    match op:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left*right
        case "/":
            return left/right
        case "ln":
            return math.log(right)
        case "sin":
            return math.sin(right)
        case "cos":
            return math.cos(right)
        case "tg":
            return math.tan(right)
        case "ctg":
            return 1/math.tan(right)
        case "exp":
            return math.exp(right)
        case "sqrt":
            return math.sqrt(right)
        case "^":
            return left**right


def is_unary(op: str) -> bool:
    return op in ["ln", "sin", "cos", "tg", "ctg", "exp", "sqrt"]


def get_var_val(v: str, other_vars: dict) -> str:
    if v in other_vars:
        return other_vars[v]
    else:
        match v:
            case "e":
                return repr(math.e)
            case "pi":
                return repr(math.pi)
            case _:
                return None


def is_variable(v: str, var_dict: dict) -> bool:
    return get_var_val(v, var_dict) is not None


# @logger.logger
def str_to_float(var_dict: dict):
    def foo(s: str) -> float:
        s = s.strip()
        val = get_var_val(s, var_dict)
        if val is None:
            val = float(s)
        else:
            val = float(val)
        return val
    return foo
