from unittest import expectedFailure

from .. utils import TranspileTestCase, UnaryOperationTestCase, BinaryOperationTestCase, InplaceOperationTestCase


class ObjectTests(TranspileTestCase):
    @expectedFailure
    def test_setitem(self):
        self.assertCodeExecution("""
            class MyClass:
                def __setitem__(self, key, item):
                    print("In __setitem__")

            obj = MyClass()
            obj[0] = 0
            """)

    def test_getitem(self):
        self.assertCodeExecution("""
            class MyClass:
                def __getitem__(self, key):
                    print("In __getitem__")

            obj = MyClass()
            print(obj[0])
            """)

    @expectedFailure
    def test_getattribute(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj = MyClass()
            try:
                print(obj.a)
            except AttributeError as e:
                print(e)

            class MyClass1:
                def __getattribute__(self, name):
                    return name

            obj = MyClass1()
            print(obj.a)
        """)

    @expectedFailure
    def test_getattr(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj = MyClass()
            try:
                print(obj.a)
            except AttributeError as e:
                print(e)

            class MyClass1:
                def __getattr__(self, name):
                    return name

            obj = MyClass1()
            print(obj.a)
        """)

    @expectedFailure
    def test_hash(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj = MyClass()
            hash_code = obj.hash()
            print(isinstance(hash_code, int))
        """)

    @expectedFailure
    def test_repr(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj = MyClass()
            print(obj.repr())

            class MyClass1:
                def __repr__(self):
                    return "I am a MyClass1!"

            obj = MyClass1()
            print(obj.repr())
        """)

    def test_bytes(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj = MyClass()
            try:
                print(bytes(obj))
            except TypeError as e:
                print(e)
        """)

    def test_eq(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj1 = MyClass()
            obj2 = MyClass()
            print(obj1 == obj2)
            print(obj1 is obj2)

            class MyClass1:
                def __eq__(self, other):
                    return True

            obj1 = MyClass1()
            obj2 = MyClass1()
            print(obj1 == obj2)
            print(obj1 is obj2)
        """)

    def test_le(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj1 = MyClass()
            obj2 = MyClass()
            try:
                print(obj1 <= obj2)
            except TypeError as e:
                print(e)

            class MyClass1:
                def __le__(self, other):
                    return True

            obj1 = MyClass1()
            obj2 = MyClass1()
            print(obj1 <= obj2)
        """)

    def test_lt(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj1 = MyClass()
            obj2 = MyClass()
            try:
                print(obj1 < obj2)
            except TypeError as e:
                print(e)

            class MyClass1:
                def __lt__(self, other):
                    return True

            obj1 = MyClass1()
            obj2 = MyClass1()
            print(obj1 < obj2)
        """)

    def test_ge(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj1 = MyClass()
            obj2 = MyClass()
            try:
                print(obj1 >= obj2)
            except TypeError as e:
                print(e)

            class MyClass1:
                def __ge__(self, other):
                    return True

            obj1 = MyClass1()
            obj2 = MyClass1()
            print(obj1 >= obj2)
        """)

    def test_gt(self):
        self.assertCodeExecution("""
            class MyClass:
                pass

            obj1 = MyClass()
            obj2 = MyClass()
            try:
                print(obj1 > obj2)
            except TypeError as e:
                print(e)

            class MyClass1:
                def __gt__(self, other):
                    return True

            obj1 = MyClass1()
            obj2 = MyClass1()
            print(obj1 > obj2)
        """)


class UnaryObjectOperationTests(UnaryOperationTestCase, TranspileTestCase):
    data_type = 'obj'

    not_implemented = [
        'test_unary_not'
    ]


class BinaryObjectOperationTests(BinaryOperationTestCase, TranspileTestCase):
    data_type = 'obj'

    not_implemented = [
        'test_xor_class',
        'test_true_divide_class',
        'test_subtract_class',
        'test_subscr_class',
        'test_lshift_class',
        'test_rshift_class',
        'test_power_class',
        'test_or_class',
        'test_multiply_class',
        'test_modulo_class',
        'test_lt_class',
        'test_gt_class',
        'test_ge_class',
        'test_le_class',
        'test_add_class',
        'test_and_class',
        'test_floor_divide_class'
    ]

    is_flakey = [
        'test_eq_class',
        'test_ne_class',
    ]



class InplaceObjectOperationTests(InplaceOperationTestCase, TranspileTestCase):
    data_type = 'obj'

    not_implemented = [
        'test_multiply_tuple',
        'test_multiply_str',
        'test_multiply_list',
        'test_multiply_bytes',
        'test_multiply_bytearray',

        'test_xor_class',
        'test_true_divide_class',
        'test_subtract_class',
        'test_rshift_class',
        'test_power_class',
        'test_or_class',
        'test_multiply_class',
        'test_modulo_class',
        'test_lshift_class',
        'test_floor_divide_class',
        'test_and_class',
        'test_add_class',
    ]
