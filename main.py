import sys

from funcBuilders import *
from parser import *
from calc import *


def read_constants() -> dict:
    inp = input("Input constants: ")
    var_dict = {}
    while (inp != '.') and (inp.strip() != ""):
        name, val = inp.split('=')
        name.strip()
        val.strip()
        var_dict[name] = val
        inp = input("Input constants: ")
    return var_dict


def calc_integral():
    var_dict = read_constants()
    s = input("Input function: ").replace("\\", "/")
    s = f"({s})"
    a, b = map(str_to_float(var_dict), input("Input limits: ").split())
    print()
    polish = translate(s)
    print(f"Integral(eps={0.001:.3f}) : {integral(build_fx(polish, var_dict), a, b):.3f}")


def calc_func():
    # var_dict = read_constants()
    var_dict = {}
    print("Running with empty var_dict", file=sys.stderr)
    s = input("Input function: ").replace("\\", "/")
    s = f"({s})"
    print()
    polish = translate(s)
    print(f"Result: {calculate(polish, var_dict)}")


if __name__ == '__main__':
    # calc_integral()
    calc_func()
