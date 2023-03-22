from .. utils import TranspileTestCase, UnaryOperationTestCase, BinaryOperationTestCase, InplaceOperationTestCase


class BytearrayTests(TranspileTestCase):
    def test_setattr(self):
        self.assertCodeExecution("""
            x = bytearray([1,2,3])
            try:
                x.attr = 42
            except AttributeError as err:
                print(err)
            """)

    def test_getattr(self):
        self.assertCodeExecution("""
            x = bytearray([1,2,3])
            try:
                print(x.attr)
            except AttributeError as err:
                print(err)
            """)

    def test_contains(self):
        self.assertCodeExecution("""
            print(bytearray([1,2,3]) in bytearray([1,2]))
            print(bytearray([1,2]) in bytearray([1,2,3]))
            print(bytearray([1,2,4]) in bytearray([1,2,3]))
            print(bytearray([8,9,0,1]) in bytearray([1,2,3]))
            print(101 in bytearray([1,2,3]))
            print(101 in bytearray([1,2,3,101]))
            print(b'pybee' in bytearray([1,2]))
            print(bytearray([1,2]) in b'pybee')
        """)
        self.assertCodeExecution("""
            try:
                print(300 in bytearray([1,2,3]))
                print("No error raised")
            except ValueError:
                print("Raised a ValueError")
        """)
        self.assertCodeExecution("""
            try:
                print(['b', 'e'] in bytearray([1,2,3]))
                print("No error raised")
            except TypeError:
                print("Raised a TypeError")
        """)

    def test_capitalize(self):
        self.assertCodeExecution("""
            print(bytearray(b'abc').capitalize())
            print(bytearray().capitalize())
        """)

    def test_islower(self):
        # TODO: add this test when adding support for literal hex bytes
        # print(b'\xf0'.islower())

        self.assertCodeExecution("""
            print(bytearray(b'abc').islower())
            print(bytearray(b'').islower())
            print(bytearray(b'Abccc').islower())
            print(bytearray(b'HELLO WORD').islower())
            print(bytearray(b'@#$%!').islower())
            print(bytearray(b'hello world').islower())
            print(bytearray(b'hello world   ').islower())
        """)

    def test_isspace(self):
        self.assertCodeExecution("""
            print(bytearray(b'testupper').isspace())
            print(bytearray(b'test isspace').isspace())
            print(bytearray(b' ').isspace())
            print(bytearray(b'').isspace())
            print(bytearray(b'\x46').isspace())
            print(bytearray(b'   \t\t').isspace())
            print(bytearray(b' \x0b').isspace())
            print(bytearray(b' \f').isspace())
            print(bytearray(b' \\n').isspace())
            print(bytearray(b' \\r').isspace())
        """)

    def test_upper(self):
        # TODO: add this test when adding support for literal hex bytes
        # print(bytearray(b'\xf0').upper())

        self.assertCodeExecution("""
            print(bytearray(b'abc').upper())
            print(bytearray(b'').upper())
            print(bytearray(b'Abccc').upper())
            print(bytearray(b'HELLO WORD').upper())
            print(bytearray(b'@#$%!').upper())
            print(bytearray(b'hello world').upper())
            print(bytearray(b'hello world   ').upper())
        """)

    def test_ljust(self):
        self.assertCodeExecution("""
            print(bytearray(b'testMoreThanWidth').ljust(5))
            print(bytearray(b'testEqualWidth').ljust(14))
            print(bytearray(b'testLessThanWidth').ljust(20))
            print(bytearray(b'testMoreWithFill').ljust(2, b'x'))
            print(bytearray(b'testEqualWithFill').ljust(17, b'x'))
            print(bytearray(b'testLessWithFill').ljust(25, b'x'))
            print(bytearray(b'testNegative').ljust(-20))
            print(bytearray(b'').ljust(5))
            print(bytearray(b'testNoChangeWidthOne').ljust(True, b'x'))
            print(bytearray(b'testBArraySecondArg').ljust(True, bytearray(b'x')))
            try:
                print(bytearray(b'testStrArgError').ljust('5'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testMoreLengthError').ljust(12, b'as'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testStrFillingChar').ljust(12, 'a'))
            except Exception as e:
                print(str(e))
        """)

    def test_rjust(self):
        self.assertCodeExecution("""
            print(bytearray(b'testMoreThanWidth').rjust(5))
            print(bytearray(b'testEqualWidth').rjust(14))
            print(bytearray(b'testLessThanWidth').rjust(20))
            print(bytearray(b'testMoreWithFill').rjust(2, b'x'))
            print(bytearray(b'testEqualWithFill').rjust(17, b'x'))
            print(bytearray(b'testLessWithFill').rjust(25, b'x'))
            print(bytearray(b'testNegative').rjust(-20))
            print(bytearray(b'').rjust(5))
            print(bytearray(b'testNoChangeWidthOne').rjust(True, b'x'))
            print(bytearray(b'testBArraySecondArg').rjust(True, bytearray(b'x')))
            try:
                print(bytearray(b'testStrArgError').rjust('5'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testMoreLengthError').rjust(12, b'as'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testStrFillingChar').rjust(12, 'a'))
            except Exception as e:
                print(str(e))
        """)

    def test_expandtabs(self):
        self.assertCodeExecution("""
            print(bytearray(b'testNoTabs').expandtabs())
            print(bytearray(b'test\t').expandtabs())
            print(bytearray(b'testDoubleTab\t\t').expandtabs())
            print(bytearray(b'testTab\tandText').expandtabs())
            print(bytearray(b'testTab\t').expandtabs(4))
            print(bytearray(b'testTab\t\t').expandtabs(4))
            print(bytearray(b'test\t\t').expandtabs(-4))
            print(bytearray(b'').expandtabs(5))
            try:
                print(bytearray(b'testErrorChar\t').expandtabs('a'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testErrorChars\t').expandtabs('as'))
            except Exception as e:
                print(str(e))
            try:
                print(bytearray(b'testErrorCharNum\t').expandtabs('1'))
            except Exception as e:
                print(str(e))
        """)

    def test_isalpha(self):
        # TODO: add this test when adding support for literal hex bytes
        # print(bytearray(b'\xf0').isalpha())

        self.assertCodeExecution("""
            print(bytearray(b'abc').isalpha())
            print(bytearray(b'').isalpha())
            print(bytearray(b'Abccc').isalpha())
            print(bytearray(b'HELLO WORD').isalpha())
            print(bytearray(b'@#$%!').isalpha())
            print(bytearray(b'hello world').isalpha())
            print(bytearray(b'hello world   ').isalpha())
        """)

    def test_isupper(self):
        self.assertCodeExecution("""
            print(bytearray(b'abc').isupper())
            print(bytearray(b'ABC').isupper())
            print(bytearray(b'').isupper())
            print(bytearray(b'Abccc').isupper())
            print(bytearray(b'HELLO WORD').isupper())
            print(bytearray(b'@#$%!').isupper())
            print(bytearray(b'hello world').isupper())
            print(bytearray(b'hello world   ').isupper())
        """)

    def test_lower(self):
        self.assertCodeExecution("""
            print(bytearray(b"abc").lower())
            print(bytearray(b"HELLO WORLD!").lower())
            print(bytearray(b"hElLO wOrLd").lower())
            print(bytearray(b"[Hello] World").lower())
            """)

    def test_count(self):
        self.assertCodeExecution("""
            print(bytearray(b'abcabca').count(97))
            print(bytearray(b'abcabca').count(b'abc'))
            print(bytearray(b'qqq').count(b'q'))
            print(bytearray(b'qqq').count(b'qq'))
            print(bytearray(b'qqq').count(b'qqq'))
            print(bytearray(b'qqq').count(b'qqqq'))
            print(bytearray(b'abcdefgh').count(b'bc',-7, -5))
            print(bytearray(b'abcdefgh').count(b'bc',1, -5))
            print(bytearray(b'abcdefgh').count(b'bc',0, 3))
            print(bytearray(b'abcdefgh').count(b'bc',-7, 500))
            print(bytearray(b'qqaqqbqqqcqqqdqqqqeqqqqf').count(b'qq'),1)
            print(bytearray(b'').count(b'q'),0)
        """)

    def test_find(self):
        self.assertCodeExecution("""
            print(bytearray(b'').find(b'a'))
            print(bytearray(b'abcd').find(b''))
            print(bytearray(b'abcd').find(b'...'))
            print(bytearray(b'abcd').find(b'a'))
            print(bytearray(b'abcd').find(b'b'))
            print(bytearray(b'abcd').find(b'c'))
            print(bytearray(b'abcd').find(b'd'))
            print(bytearray(b'abcd').find(bytearray(b'ab')))
            print(bytearray(b'abcd').find(b'bc'))
            print(bytearray(b'abcd').find(b'cd'))
            print(bytearray(b'abcd').find(b'cd', 2))
            print(bytearray(b'abcd').find(bytearray(b'ab'), 3))
            print(bytearray(b'abcd').find(b'cd', 2, 3))
            print(bytearray(b'abcd').find(bytearray(b'ab'), 3, 4))
        """)

    def test_center(self):
        self.assertCodeExecution("""
            print(bytearray(b'pybee').center(12))
            print(bytearray(b'pybee').center(13))
            print(bytearray(b'pybee').center(2))
            print(bytearray(b'pybee').center(2, b'a'))
            print(bytearray(b'pybee').center(12, b'a'))
            print(bytearray(b'pybee').center(13, b'a'))
            print(bytearray(b'pybee').center(-5))
            print(bytearray(b'').center(5))
            print(bytearray(b'pybee').center(True, b'a'))
            print(bytearray(b'pybee').center(True, bytearray(b'a')))
        """)

    def test_title(self):
        self.assertCodeExecution(r"""
            print(bytearray(b"").title())
            print(bytearray(b"abcd").title())
            print(bytearray(b"NOT").title())
            print(bytearray(b"coca cola").title())
            print(bytearray(b"they are from UK, are they not?").title())
            print(bytearray(b'/@.').title())
            print(bytearray(b'\x46\x55\x43\x4B').title())
            print(bytearray(b"py.bee").title())
        """)

    def test_istitle(self):
        self.assertCodeExecution(r"""
            print(bytearray(b"").istitle())
            print(bytearray(b"abcd").istitle())
            print(bytearray(b"NOT").istitle())
            print(bytearray(b"coca cola").istitle())
            print(bytearray(b"they are from UK, are they not?").istitle())
            print(bytearray(b'/@.').istitle())
            print(bytearray(b'\x46\x55\x43\x4B').istitle())
            print(bytearray(b"py.bee").title())
        """)

    def test_repr(self):
        self.assertCodeExecution(r"""
            print(repr(bytearray(b'\xc8')))
            print(repr(bytearray(b'abcdef \xc8 abcdef')))
            print(repr(bytearray(b'abcdef \xc8 abcdef\n\r\t')))
            print(bytearray(b'abcdef \xc8 abcdef\n\r\t'))
            for b in range(0, 256, 16):
                print(repr(bytearray(range(b, b+16))))
            for b in range(0, 256, 16):
                print(bytearray(range(b, b+16)))
        """)

    def test_endswith(self):
        self.assertCodeExecution(r"""
            print(bytearray(b'banana').endswith(b'ana'))
            print(bytearray(b'banana').endswith(b''))
            print(bytearray(b'').endswith(b'ana'))
            print(bytearray(b'').endswith(b''))
        """)

    def test_startswith(self):
        self.assertCodeExecution(r"""
            print(bytearray(b'banana').startswith(b'ana'))
            print(bytearray(b'banana').startswith(b''))
            print(bytearray(b'').startswith(b'ana'))
            print(bytearray(b'').startswith(b''))
        """)

    def test_isalnum(self):
        self.assertCodeExecution("""
            print(bytearray(b'0').isalnum())
            print(bytearray(b'9').isalnum())
            print(bytearray(b'1234567890').isalnum())
            print(bytearray(b'89A23gM23z').isalnum())
            print(bytearray(b':923').isalnum())
            print(bytearray(b'\\923').isalnum())
            print(bytearray(b' jdf fhd 33').isalnum())
            print(bytearray(b'@#$%^&*').isalnum())
            print(bytearray(b'"478\t47ads:').isalnum())
            print(bytearray(b'AbZ').isalnum())
        """)

    def test_isdigit(self):
        self.assertCodeExecution("""
            print(bytearray(b'0').isdigit())
            print(bytearray(b'9').isdigit())
            print(bytearray(b'1234567890').isdigit())
            print(bytearray(b'8923g23823').isdigit())
            print(bytearray(b'923').isdigit())
            print(bytearray(b'\\923').isdigit())
            print(bytearray(b'000').isdigit())
            print(bytearray(b'@#$%^&*').isdigit())
            print(bytearray(b'"478\t47ads:').isdigit())
            print(bytearray(b'AbZ').isdigit())
        """)

    def test_join(self):
        self.assertCodeExecution("""
            b = bytearray(b'.')
            print(b.join([b'12', b'dh']))
            print(b.join([bytearray(b'12'), bytearray(b'dh')]))
            b = bytearray(b' ')
            print(b.join([b'd', bytearray(b'l22-'), b'=ej*']))
            print(b.join([bytearray(b'31'), b'`', b'^']))
            print(b.join([bytearray(b'dh')]))
            b = bytearray(b'%#@!')
            print(b.join([b'1',b'd',b'<']))
            print(b.join([b'12']))
        """)


class UnaryBytearrayOperationTests(UnaryOperationTestCase, TranspileTestCase):
    data_type = 'bytearray'


class BinaryBytearrayOperationTests(BinaryOperationTestCase, TranspileTestCase):
    data_type = 'bytearray'

    not_implemented_versions = {
        'test_modulo_complex': (3.4, ),
    }


class InplaceBytearrayOperationTests(InplaceOperationTestCase, TranspileTestCase):
    data_type = 'bytearray'

    not_implemented_versions = {
        'test_modulo_complex': (3.4, ),
    }
