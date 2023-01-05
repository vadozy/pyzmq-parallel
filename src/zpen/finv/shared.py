import time


def f1(**kwargs):
    time.sleep(0.5)
    print(f"f1: {kwargs}")


class C1:
    def __init__(self, name):
        self.name = name

    def f1(self, **kwargs):
        time.sleep(0.1)
        print(f"bound f1: {self.name} {kwargs}")
        return 42
