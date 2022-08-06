from contextlib import contextmanager


class _Comparison:
    def __init__(self, var, op, value):
        self.var = var
        self.op = op
        self.value = value

    def __repr__(self) -> str:
        return f"Comparing var({self.var!r}) {self.op} {self.value!r}"


class _Increment:
    def __init__(self, var, op, value):
        self.var = var
        self.op = op
        self.value = value

    def __repr__(self) -> str:
        return f"Incrementing var({self.var!r}) with {self.op}{self.value!r}"


class var:
    def __init__(self, value):
        self.value = value

    def __lt__(self, value):
        return _Comparison(var=self, op="<", value=value)

    def __add__(self, value):
        return _Increment(var=self, op="+", value=value)


@contextmanager
def _for(variable, comparison, increment):
    actual_value = variable.value
    var_class = type(variable)

    # So Python doesn't allow this. Also, we're already modifying the `var`
    # class itself, which makes this path very fragile to begin with.
    var_class.__dict__ = {}
    var_class.__getattr__ = lambda attr: getattr(actual_value, attr)
    yield


with _for(i := var(0), i < 10, i + 2):
    print(i)
    print(i + 2)
    print(i < 5)
    print(isinstance(i, int))
