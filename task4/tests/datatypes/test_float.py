from .. utils import (
    TranspileTestCase,
    UnaryOperationTestCase,
    BinaryOperationTestCase,
    InplaceOperationTestCase,
    SAMPLE_SUBSTITUTIONS
)


class FloatTests(TranspileTestCase):
    def test_setattr(self):
        self.assertCodeExecution("""
            x = 3.14159
            try:
                x.attr = 42
            except AttributeError as err:
                print(err)
            """)

    def test_getattr(self):
        self.assertCodeExecution("""
            x = 3.14159
            try:
                print(x.attr)
            except AttributeError as err:
                print(err)
            """)

    def test_setitem(self):
        self.assertCodeExecution("""
            x = 3.14159
            try:
                x[0] = 2
            except TypeError as err:
                print(err)
        """)

    def test_repr(self):
        self.assertCodeExecution("""
            x = 350000000000000000.0
            print(x)
            x = 3500.0
            print(x)
            x = 35.0
            print(x)
            x = 3.5
            print(x)
            x = 0.35
            print(x)
            x = 0.035
            print(x)
            x = 0.0035
            print(x)
            x = 0.00035
            print(x)
            x = 0.000035
            print(x)
            x = 0.0000035
            print(x)
            x = 0.00000000000000035
            print(x)

            x = 0.0
            print(x)
            x = float('-0.0')
            print(x)
            x = float('nan')
            print(x)
            x = float('inf')
            print(x)
            x = float('-inf')
            print(x)
            """)

    def test_negative_zero_constant(self):
        self.assertCodeExecution("""
            x = -0.0
            y = 0.0
            print(x, y)
            """)

    def test_is_integer(self):
        self.assertCodeExecution("""
            x = 0.0
            print(x.is_integer())
            x = 3.14
            print(x.is_integer())
            x = -1.0
            print(x.is_integer())
            x = -62.5
            print(x.is_integer())
            x = float('nan')
            print(x.is_integer())
            x = float('inf')
            print(x.is_integer())
            x = float('-inf')
            print(x.is_integer())
            """)

    def test_hex(self):
        numbers = [
            0e0, -0e0, 10000152587890625e-16, -566e85,
            -87336362425182547697e-280, 4.9406564584124654e-324,
            'nan', 'inf', '-inf'
        ]
        template = """
            x = float('{}')
            print(x.hex())
            """
        code = '\n'.join(template.format(number) for number in numbers)
        self.assertCodeExecution(code)

    def test_mul_TypeError(self):
        self.assertCodeExecution("""
            a = 5.6
            try:
                print(a*None);
            except TypeError as e:
                print(e)
            """)

    def test_none(self):
        self.assertCodeExecution("""
            try:
                print(float(None))
            except TypeError as err:
                print(err)
        """)

    def test_no_arguments(self):
        self.assertCodeExecution("""
            print(float())
        """)

    def test_too_many_arguments(self):
        self.assertCodeExecution("""
            try:
                print(float(1, 2))
            except TypeError as err:
                print(err)
        """)


class UnaryFloatOperationTests(UnaryOperationTestCase, TranspileTestCase):
    data_type = 'float'

    not_implemented = [
    ]


class BinaryFloatOperationTests(BinaryOperationTestCase, TranspileTestCase):
    data_type = 'float'

    substitutions = {
        "(-0.8946025309573877+0.446862743585361j)": [
            "(-0.8946025309573877+0.44686274358536093j)"
        ]
    }

    substitutions.update(SAMPLE_SUBSTITUTIONS)

    not_implemented = [
    ]


class InplaceFloatOperationTests(InplaceOperationTestCase, TranspileTestCase):
    data_type = 'float'

    substitutions = {
        "(-0.8946025309573877+0.446862743585361j)": [
            "(-0.8946025309573877+0.44686274358536093j)"
        ]
    }

    substitutions.update(SAMPLE_SUBSTITUTIONS)

    not_implemented = [
    ]
