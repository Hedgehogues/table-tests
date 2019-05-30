class MyClass:

    def __init__(self, a):
        self.a = a

    def plus(self, b):
        return self.a + b

    def raise_(self, b):
        raise Exception("MyClass")


def plus(a, b):
    return a + b
