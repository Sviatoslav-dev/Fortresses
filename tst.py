class A:
    def __init__(self, a):
        self.a = a

    def __del__(self):
        pass


c = [A(2), A(3)]

b = [c[1], A(4)]

# c[1].__del__()
del c[1]

print(b)
