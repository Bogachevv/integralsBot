from operators import *


def integral(func, a: float, b: float, eps=0.001):
    s = (func(a) + func(b)) / 2
    h = (b-a)/8
    x = a
    while x+h < b:
        x += h
        s += func(x)
    cur_int = s*h
    prev_int = cur_int
    flag = True
    while flag or (abs(cur_int - prev_int) > eps):
        x = a - h/2
        while x + h < b:
            x += h
            s += func(x)
        h = h/2
        prev_int = cur_int
        cur_int = s * h
        flag = False
    return cur_int


def calculate(polish: list[str], var_dict: dict = None):
    stack = []
    var_dict = {} if var_dict is None else var_dict
    for op in polish:
        if is_operator(op):
            right = float(stack.pop())
            left = None if is_unary(op) else float(stack.pop())
            stack.append(calc_operation(op, left, right))
        elif is_variable(op, var_dict):
            stack.append(get_var_val(op, var_dict))
        else:
            stack.append(op)
    assert len(stack) == 1
    return stack.pop()
