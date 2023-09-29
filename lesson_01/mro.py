class A:
    def foo(self):
        print("foo from A")  # noqa: T201


class B(A):
    def foo(self):
        print("foo from B")  # noqa: T201


class C(A):
    def foo(self):
        print("foo from C")  # noqa: T201


class D(B, C):
    def foo(self):
        super(C, self).foo()


if __name__ == "__main__":
    instance = D()
    instance.foo()  # --> foo from A

# super(--class(клас, для якого викликати наступний в MRO),
#       --self(екземпляр класу)) – повторення логіки батьківського класу,
# дозволяє отримувати наступний з об'єктів MRO
# В залежності від того, який об'єкт створено, такий і буде результат super()
# C3 - алгоритм пошуку, суміш між пошуком в глибину та ширину
