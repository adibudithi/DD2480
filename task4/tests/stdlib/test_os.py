import unittest

from ..utils import TranspileTestCase


class OsModuleTests(TranspileTestCase):
    def test_getenv(self):
        self.assertCodeExecution("""
            import os
            print(os.getenv('USER'))
            print(os.getenv('NOT_HERE', default='something'))
            print(os.getenv('NOT_HERE', 'something'))
            print(os.getenv('NOT_HERE'))
            """)
        self.assertCodeExecution("""
            import os
            try:
                print(os.getenv(None))
            except Exception as e:
                print(type(e), e)
            try:
                print(os.getenv(1))
            except Exception as e:
                print(type(e), e)
            try:
                print(os.getenv())
            except Exception as e:
                print(type(e), e)
            """)

    @unittest.expectedFailure
    def test_getcwd(self):
        self.assertCodeExecution("""
            import os
            print(os.getcwd())
        """)

    def test_cpu_count(self):
        self.assertCodeExecution("""
            import os
            print(os.cpu_count())
        """)
