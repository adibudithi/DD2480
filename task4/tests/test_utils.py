import unittest

from .utils import adjust, cleanse_java, cleanse_python, TranspileTestCase


class AdjustTests(unittest.TestCase):
    def assertEqualOutput(self, actual, expected):
        self.assertEqual(adjust(actual), adjust(expected))

    def test_adjust(self):
        "Test input can be stripped of leading spaces."
        self.assertEqual("""for i in range(0, 10):
    print('hello, world')
print('Done.')
""", adjust("""
            for i in range(0, 10):
                print('hello, world')
            print('Done.')
        """))

    def test_adjust_no_leading_space(self):
        self.assertEqual("""for i in range(0, 10):
    print('hello, world')
print('Done.')
""", adjust("""for i in range(0, 10):
    print('hello, world')
print('Done.')
"""))


class AssertCodeExecutionTests(TranspileTestCase):
    @unittest.expectedFailure
    def test_fail_unexpected_exception(self):
        self.assertCodeExecution("""
            raise ValueError
            """)

    def test_allow_expected_exception(self):
        self.assertCodeExecution("""
            raise ValueError
            """, exits_early=True)

    @unittest.expectedFailure
    def test_fail_missing_expected_exception(self):
        self.assertCodeExecution("""
            print('Done.')
            """, exits_early=True)


class JavaNormalizationTests(unittest.TestCase):
    def assertNormalized(self, actual, expected):
        self.assertEqual(cleanse_java(adjust(actual), None), adjust(expected))

    def test_no_exception(self):
        self.assertNormalized(
            """
            Hello, world.
            """,
            """
            Hello, world.
            """
        )

    def test_exception_in_clinit(self):
        self.assertNormalized(
            """
            Exception in thread "main" java.lang.ExceptionInInitializerError
            Caused by: IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.<clinit>(test.py:2)
            """,
            """
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:2
            """
        )

    def test_exception_in_module_init(self):
        self.assertNormalized(
            """
            Exception in thread "main" NameError: name 'y' is not defined
                at org.python.types.Module.__getattribute__(Module.java:32)
                at python.example.__init__.module$import(example.py:2)
                at python.example.__init__.main(example.py)
            """,
            """
            ### EXCEPTION ###
            NameError: name 'y' is not defined
                example.py:2
            """
        )

    def test_exception_in_clinit_after_output(self):
        self.assertNormalized(
            """
            Hello, world.
            Exception in thread "main" java.lang.ExceptionInInitializerError
            Caused by: IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.<clinit>(test.py:2)
            """,
            """
            Hello, world.
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:2
            """
        )

    def test_exception_in_clinit_after_output_windows(self):
        self.assertNormalized(
            """
            Hello, world.
            java.lang.ExceptionInInitializerError
            Caused by: IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.<clinit>(test.py:2)
            """,
            """
            Hello, world.
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:2
            """
        )

    def test_exception_in_clinit_after_output_testdaemon(self):
        self.assertNormalized(
            """
            False
            True
            Exception in thread "main" java.lang.ExceptionInInitializerError
            \tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
            \tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
            \tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
            \tat java.lang.reflect.Method.invoke(Method.java:497)
            \tat python.testdaemon.TestDaemon.main(TestDaemon.java:66)
            Caused by: KeyError: 'c'
                at org.python.types.Dict.__getitem__(Dict.java:142)
                at python.test.__init__.<clinit>(test.py:4)
                ... 5 more
            """,
            """
            False
            True
            ### EXCEPTION ###
            KeyError: 'c'
                test.py:4
            """
        )

    def test_exception_in_method(self):
        self.assertNormalized(
            """
            Exception in thread "main" IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.main(test.py:3)
            """,
            """
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:3
            """
        )

    def test_exception_in_method_windows(self):
        self.assertNormalized(
            """
            IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.main(test.py:3)
            """,
            """
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:3
            """
        )

    def test_exception_in_method_after_output(self):
        self.assertNormalized(
            """
            Hello, world.
            Exception in thread "main" IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.main(test.py:3)
            """,
            """
            Hello, world.
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:3
            """
        )

    def test_exception_in_method_after_output_windows(self):
        self.assertNormalized(
            """
            Hello, world.
            IndexError: list index out of range
                at org.python.types.List.__getitem__(List.java:100)
                at org.python.types.List.__getitem__(List.java:85)
                at python.test.main(test.py:3)
            """,
            """
            Hello, world.
            ### EXCEPTION ###
            IndexError: list index out of range
                test.py:3
            """
        )

    def test_exception_in_constructor(self):
        self.assertNormalized(
            """
            Exception in thread "main" java.lang.ExceptionInInitializerError
            Caused by: UnboundLocalError: local variable 'x' referenced before assignment
              at python.example.Foo.__init__(example.py:44)
              at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
              at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
              at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
              at java.lang.reflect.Method.invoke(Method.java:606)
              at org.python.types.Method.invoke(Method.java:66)
              at python.example.Foo.<init>(example.py)
              at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
              at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:57)
              at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
              at java.lang.reflect.Constructor.newInstance(Constructor.java:526)
              at org.python.types.Constructor.invoke(Constructor.java:25)
              at python.example.<clinit>(example.py:51)
            """,
            """
            ### EXCEPTION ###
            UnboundLocalError: local variable 'x' referenced before assignment
                example.py:51
                example.py:44
            """
        )

    def test_memory_reference(self):
        self.assertNormalized(
            """
            Class is <class 'com.example.MyClass'>
            Method is <native function com.example.MyClass.method>
            Method from instance is <bound native method com.example.MyClass.method of <Native class com.example.MyClass object at 0x1eb19f4e>>
            Hello from the instance!
            Done.
            """,  # noqa
            """
            Class is <class 'com.example.MyClass'>
            Method is <native function com.example.MyClass.method>
            Method from instance is <bound native method com.example.MyClass.method of <Native class com.example.MyClass object at 0xXXXXXXXX>>
            Hello from the instance!
            Done.
            """  # noqa
        )


class PythonNormalizationTests(unittest.TestCase):
    def assertNormalized(self, actual, expected):
        self.assertEqual(cleanse_python(adjust(actual), None), adjust(expected))

    def test_no_exception(self):
        self.assertNormalized(
            """
            Hello, world.
            """,
            """
            Hello, world.
            """
        )

    def test_exception(self):
        self.assertNormalized(
            """
            Traceback (most recent call last):
              File "test.py", line 3, in <module>
                print(x & y)
            TypeError: unsupported operand type(s) for &: 'float' and 'bool'
            """,
            """
            ### EXCEPTION ###
            TypeError: unsupported operand type(s) for &: 'float' and 'bool'
                test.py:3
            """
        )

    def test_exception_with_other_text(self):
        self.assertNormalized(
            """
            Hello, world.
            Traceback (most recent call last):
              File "test.py", line 3, in <module>
                print(x & y)
            TypeError: unsupported operand type(s) for &: 'float' and 'bool'
            """,
            """
            Hello, world.
            ### EXCEPTION ###
            TypeError: unsupported operand type(s) for &: 'float' and 'bool'
                test.py:3
            """
        )

    def test_memory_reference(self):
        self.assertNormalized(
            """
            Class is <class 'com.example.MyClass'>
            Method is <native function com.example.MyClass.method>
            Method from instance is <bound native method com.example.MyClass.method of <Native class com.example.MyClass object at 0x1eb19f4e>>
            Hello from the instance!
            Done.
            """,  # noqa
            """
            Class is <class 'com.example.MyClass'>
            Method is <native function com.example.MyClass.method>
            Method from instance is <bound native method com.example.MyClass.method of <Native class com.example.MyClass object at 0xXXXXXXXX>>
            Hello from the instance!
            Done.
            """  # noqa
        )


class JavaBootstrapTests(TranspileTestCase):
    def test_java_code(self):
        "You can supply Java code and use it from within Python"
        self.assertJavaExecution(
            """
            from com.example import MyClass

            obj = MyClass()

            obj.doStuff()

            print("Done.")
            """,
            java={
                'com/example/MyClass': """
                package com.example;

                public class MyClass {
                    public void doStuff() {
                        System.out.println("Hello from Java");
                    }
                }
                """
            },
            out="""
            Hello from Java
            Done.
            """,
        )
