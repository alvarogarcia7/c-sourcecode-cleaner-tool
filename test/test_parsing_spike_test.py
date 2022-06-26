import os
import unittest

from pycparser import parse_file, c_generator, c_ast

all_values = set()
all_values_with_coord = []

# https://github.com/eliben/pycparser/blob/master/examples/func_defs.py
class MyVisitor(c_ast.NodeVisitor):
    # def visit(self, node):
    #     print('%s at %s' % (node.decl.name, node.decl.coord))
    def visit_Decl(self, node):
        try:
            v = node.children()[1][1].exprs
            values = [int(x.value, 16) for x in v]
            values_str = "".join([str(x) for x in values])
            del v
            if values_str in all_values:
                coord = list(filter(lambda x: x['value'] == values_str, all_values_with_coord))[0]['coord']
                print(f"Duplicated value in line {node.coord}. Present in {coord.file}:{coord.line}:{coord.column}")
                return
            # print(node.name)
            all_values.add(values_str)
            all_values_with_coord.append({'value': values_str, 'coord': node.coord})
        except IndexError:
            pass
        except AttributeError:
            pass

    def visit_NamedInitializer(self, node):
        print(node)

# https://github.com/eliben/pycparser/blob/master/examples/rewrite_ast.py

def translate_to_c(filename: str) -> None:
    """ Simply use the c_generator module to emit a parsed AST.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    ast = parse_file(f"{path}/{filename}", use_cpp=True,
                     cpp_path='gcc',
                     cpp_args=['-E', rf'-I{path}/fake_libc_include'])



    # ast.show(showcoord=True)
    # generator = c_generator.CGenerator(reduce_parentheses=True)
    # generator.indent_level = 4
    # print(generator.visit(ast))

    generator = MyVisitor()
    print(generator.visit(ast))



class XTest(unittest.TestCase):
    def test_1(self) -> None:
        translate_to_c('test_chacha20.c')
