from .. utils import TranspileTestCase, BuiltinFunctionTestCase


class StrTests(TranspileTestCase):
    pass


class BuiltinStrFunctionTests(BuiltinFunctionTestCase, TranspileTestCase):
    functions = ["str"]

    not_implemented = [
        'test_class',
    ]
