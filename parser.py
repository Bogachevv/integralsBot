from operators import *


def parse_str(s: str):
    elm = ""
    is_bracket = False
    for ch in s:
        if ch == " ":
            if elm != "":
                yield elm
                elm = ""
        elif is_operator(ch) or (ch in ["(", ")"]):
            if elm != "":
                yield elm
                elm = ""
            if ch == "(":
                is_bracket = True
            elif ch == "-" and is_bracket:
                ch = "--"
            # print(f"(debug): {ch} with flag: {is_bracket}")
            yield ch
        else:
            is_bracket = False
            elm += ch


def translate(s: str):
    stack = []
    polish = []
    for ch in parse_str(s):
        if ch == "(":
            stack.append(ch)
        elif is_operator(ch):
            pr = priority(ch)
            tmp = []
            elm = stack.pop()
            while elm != '(':
                if priority(elm) >= pr:
                    polish.append(elm.strip())
                else:
                    tmp.append(elm)
                elm = stack.pop()
            stack.append(elm)
            stack.extend(reversed(tmp))
            stack.append(ch)
        elif ch == ")":
            elm = stack.pop()
            while elm != '(':
                polish.append(elm.strip())
                elm = stack.pop()
        else:
            polish.append(ch.strip())
    return polish
