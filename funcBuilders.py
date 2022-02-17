import calc


def build_func(polish: list):
    def func(**var_dict):
        return calc.calculate(polish, var_dict)

    return func


def build_fx(polish, var_dict: dict):
    def f(x: float):
        # d = {"x": x}
        d = var_dict.copy()
        d["x"] = x
        return calc.calculate(polish, d)
    return f
