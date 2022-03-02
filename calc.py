from operators import *


def integral(func, a: float, b: float, eps=0.001):
    s = (func(a) + func(b)) / 2
    n = 4
    h = (b-a)/n
    for i in range(1, n):
        s += func(a + i*h)
    cur_int = s*h
    prev_int = cur_int + 2*eps

    while abs(cur_int - prev_int) > eps:
        for i in range(n):
            s += func(a + h/2 + i*h)
        h = h/2
        n = n*2
        prev_int = cur_int
        cur_int = s * h

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
