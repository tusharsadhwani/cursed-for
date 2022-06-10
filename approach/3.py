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

    def __repr__(self) -> str:
        return repr(self.value)

    def __lt__(self, value):
        return _Comparison(var=self, op="<", value=value)

    def __add__(self, value):
        return _Increment(var=self, op="+", value=value)


i = var(0)
print(i)
print(i < 10)
print(i + 2)
