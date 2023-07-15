def f(obj):
    print(obj.a)


class A:
    def __init__(self):
        self.a = 45

    def g(self):
        f(self)

a = A()
a.g()
