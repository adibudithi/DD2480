from .. utils import TranspileTestCase, BuiltinFunctionTestCase
from unittest import expectedFailure


class OpenTests(TranspileTestCase):
    #@expectedFailure
    x = open("hello.txt", "w+")
    x.close()
    '''
    @expectedFailure
    def test_open_no_file(self):
        self.assertCodeExecution("""
            x = open()
        """)
    '''
    def test_open_file_for_reading(self):
        
        self.assertCodeExecution(""" 
            #x = open('open.txt')
            x = open('hello.txt', 'w')
        """)
    
    


class BuiltinOpenFunctionTests(BuiltinFunctionTestCase, TranspileTestCase):
    functions = ["open"]
    
    #not_implemented = ["test_bool"]

    '''not_implemented = [
        'test_bool',
        'test_bytearray',
        'test_bytes',
        'test_class',
        'test_complex',
        'test_dict',
        'test_float',
        'test_frozenset',
        'test_int',
        'test_list',
        'test_None',
        'test_NotImplemented',
        'test_range',
        'test_set',
        'test_slice',
        'test_str',
        'test_tuple',
        'test_obj',
    ]'''
