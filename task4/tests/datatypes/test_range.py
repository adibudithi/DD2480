from .. utils import TranspileTestCase, UnaryOperationTestCase, BinaryOperationTestCase, InplaceOperationTestCase


class RangeTests(TranspileTestCase):
    def test_creation(self):
        self.assertCodeExecution("""
            x = range(0, 5)
            print("x[0] = ", x[0])
            print("x[1] = ", x[1])
            print("x[3] = ", x[3])
            print("x[-1] = ", x[-1])
            try:
                print("x[5] = ", x[5])
            except IndexError as err:
                print(err)
            """)

    def test_step(self):
        self.assertCodeExecution("""
            x = range(0, 5, 2)
            print("x[0] = ", x[0])
            print("x[1] = ", x[1])
            print("x[-1] = ", x[-1])
            print("x[-3] = ", x[-3])
            try:
                print("x[3] = ", x[3])
            except IndexError as err:
                print(err)
            try:
                print("x[5] = ", x[5])
            except IndexError as err:
                print(err)
            try:
                print("x[-4] = ", x[-4])
            except IndexError as err:
                print(err)

            y = range(7, 1, -3)
            print("y[0] = ", y[0])
            print("y[1] = ", y[1])
            print("y[-2] = ", y[-2])
            """)

    def test_zero_step(self):
        self.assertCodeExecution("""
            try:
                range(0, 5, 0)
            except ValueError as err:
                print(err)
        """)

    def test_len_empty(self):
        self.assertCodeExecution("""
            print(len(range(5, 5)))
        """)

    def test_len_positive_step(self):
        self.assertCodeExecution("""
            print(len(range(5, 0, 1)))
        """)

    def test_len_negative_step(self):
        self.assertCodeExecution("""
            print(len(range(0, 5, -1)))
        """)

    def test_multiple_iterators(self):
        self.assertCodeExecution("""
            r = range(0, 10)
            print(list(r))
            print(list(r))
        """)

    def test_iterator_iterator(self):
        self.assertCodeExecution("""
            r = range(0, 10)
            i = iter(r)
            print(next(i))
            print(next(iter(i)))
            print(r)
        """)

    def test_setitem(self):
        self.assertCodeExecution("""
            r = range(10)
            try:
                r[0] = "abc"
            except TypeError as e:
                print(e)
        """)


class UnaryRangeOperationTests(UnaryOperationTestCase, TranspileTestCase):
    data_type = 'range'


class BinaryRangeOperationTests(BinaryOperationTestCase, TranspileTestCase):
    data_type = 'range'


class InplaceRangeOperationTests(InplaceOperationTestCase, TranspileTestCase):
    data_type = 'range'
