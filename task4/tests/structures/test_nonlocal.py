from unittest import expectedFailure

from ..utils import TranspileTestCase


class NonlocalTests(TranspileTestCase):
    def test_nonlocal_func(self):
        self.assertCodeExecution("""
            def func():
                a = 'a from outer'
                b = 'b from outer'
                def nested_func():
                    nonlocal a
                    print(a)
                    a = 'a from inner'
                    print(a)
                    b = 'b from inner'
                    print(b)

                nested_func()
                print(a)
                print(b)

            func()

            def func2():
                a = 'a from outer'
                b = 'b from outer'
                def nested_func2():
                    nonlocal a
                    print(a)
                    a = 'a from inner'
                    print(a)
                    def nested_nested_func():
                        nonlocal b
                        print(b)
                        b = 'b from innest'
                        print(b)

                    nested_nested_func()

                nested_func2()
                print(a)
                print(b)

            func2()
        """)

        self.assertCodeExecution("""
            def func():
                a = None
                def nested():
                    nonlocal a
                    a = 'changed by nested'
                    print(a)

                def nested2():
                    print(a)

                return (nested, nested2)

            nested, nested2 = func()
            nested2()
            nested()
            nested2()
        """)

    @expectedFailure
    def test_nonlocal_class(self):
        self.assertCodeExecution("""
            def func():
                a = 'a from outer'
                b = 'b from outer'
                class Inner():
                    nonlocal a
                    print(a)
                    a = 'a from inner'
                    b = 'b from inner'
                    print(a)
                    print(b)

                Inner()
                print(a)
                print(b)

            func()
        """)

    @expectedFailure
    def test_nonlocal_method(self):
        self.assertCodeExecution("""
            def func():
                a = 'a from outer'
                b = 'b from outer'
                class Klass:
                    def method(self):
                        nonlocal a
                        print(a)
                        a = 'a from inner'
                        print(a)
                        print(b)

                Klass().method()
                print(a)
                print(b)

            func()
        """)

    def test_nonlocal_generator(self):
        self.assertCodeExecution("""
            def func():
                a = 'a from outer'
                b = 'b from outer'
                def gen():
                    nonlocal a
                    print(a)
                    print(b)
                    a = 'a from inner'
                    yield a

                print(next(gen()))
                print(a)
                print(b)

            func()

            def func2():
                a = 'a from outer'
                b = 'b from outer'
                def gen():
                    nonlocal a
                    print(a)
                    print(b)
                    a = 'a from inner'
                    yield a

                print(next(gen()))
                print(a)
                print(b)
                yield

            next(func2())
        """)
