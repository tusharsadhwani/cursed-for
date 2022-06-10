class var:
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)


i = var(0)
print(i)
