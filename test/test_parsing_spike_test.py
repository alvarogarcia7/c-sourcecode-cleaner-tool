from __future__ import annotations

import os
import unittest
from pprint import pprint
from typing import Any, Optional

from pycparser import parse_file, c_ast


# https://github.com/eliben/pycparser/blob/master/examples/func_defs.py
class MyVisitor(c_ast.NodeVisitor):

    def __init__(self, duplicated_lines: DuplicatedLines) -> None:
        super().__init__()
        self.duplicated_lines = duplicated_lines

    # def visit(self, node):
    #     print('%s at %s' % (node.decl.name, node.decl.coord))
    def visit_Decl(self, node: Any) -> None:
        try:
            v = node.children()[1][1].exprs
            self.duplicated_lines.register_assignment(node, v)
        except IndexError:
            pass
        except AttributeError:
            pass


# https://github.com/eliben/pycparser/blob/master/examples/rewrite_ast.py

def parse_ast_of(filename: str) -> Optional[Any]:
    """ Simply use the c_generator module to emit a parsed AST.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    ast: Any | None = parse_file(f"{path}/{filename}", use_cpp=True,
                     cpp_path='gcc',
                     cpp_args=['-E', rf'-I{path}/fake_libc_include'])
    return ast


class DuplicatedLines:
    def __init__(self) -> None:
        self._list: list[Any] = []
        self._all_values: set[str] = set()
        self._all_values_with_coord: list[Any] = []

    def register_assignment(self, node: Any, v: Any) -> None:
        values = [int(x.value, 16) for x in v]
        values_str = "".join([str(x) for x in values])
        del v
        if values_str in self._all_values:
            coord = list(filter(lambda x: x['value'] == values_str, self._all_values_with_coord))[0]['coord']
            self._list.append({'new': str(node.coord), 'original': f"{coord.file}:{coord.line}:{coord.column}",
                               'variable': {'name': node.name, 'value': str(values)}})
            return
        self._all_values.add(values_str)
        self._all_values_with_coord.append({'value': values_str, 'coord': node.coord})

    @property
    def list(self) -> list[Any]:
        return self._list


class TestFindRepeatedLines(unittest.TestCase):
    def test_find_repeated_initializations(self) -> None:
        ast = parse_ast_of('sample_declarations_1.c')

        # ast.show(showcoord=True)
        # generator = c_generator.CGenerator(reduce_parentheses=True)
        # generator.indent_level = 4
        # print(generator.visit(ast))

        generator = MyVisitor(DuplicatedLines())
        generator.visit(ast)
        repeated_lines_list = generator.duplicated_lines.list
        print("")
        pprint(repeated_lines_list)
        self.assertEqual(['key__repeated', 'counter__repeated'], [x['variable']['name'] for x in repeated_lines_list])
        self.assertEqual(len(repeated_lines_list), 2)
