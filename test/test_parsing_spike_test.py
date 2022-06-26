import os
import unittest

from pycparser import parse_file, c_generator


def translate_to_c(filename: str) -> None:
    """ Simply use the c_generator module to emit a parsed AST.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    ast = parse_file(f"{path}/{filename}", use_cpp=True,
                     cpp_path='gcc',
                     cpp_args=['-E', rf'-I{path}/fake_libc_include'])
    ast.show(showcoord=True)
    generator = c_generator.CGenerator()
    print(generator.visit(ast))


class XTest(unittest.TestCase):
    def test_1(self) -> None:
        translate_to_c('test_chacha20.c')
