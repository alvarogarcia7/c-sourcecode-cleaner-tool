import os
from typing import Any, Optional

from pycparser import c_ast, parse_file

from src.duplicated_lines_repository import DuplicatedLinesRepository


class MyVisitor(c_ast.NodeVisitor):

    def __init__(self, duplicated_lines: DuplicatedLinesRepository) -> None:
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


class MyVisitor2(c_ast.NodeVisitor):

    def __init__(self, duplicated_lines: DuplicatedLinesRepository) -> None:
        super().__init__()
        self.duplicated_lines = duplicated_lines
        self._parallel_ast: list[Any] = []

    def visit(self, node):
        self._parallel_ast.append(node)
        return node

    # def visit(self, node):
    #     print('%s at %s' % (node.decl.name, node.decl.coord))
    def visit_Decl(self, node: Any) -> None:
        try:
            v = node.children()[1][1].exprs
            self.duplicated_lines.register_assignment_and_maybe_remove_it(node, v)
        except IndexError:
            pass
        except AttributeError:
            pass


def parse_ast_of(filename: str) -> Optional[Any]:
    """ Simply use the c_generator module to emit a parsed AST.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    ast: Optional[Any] = parse_file(filename, use_cpp=True,
                                    cpp_path='gcc',
                                    cpp_args=['-E', rf'-I{path}/fake_libc_include'])
    return ast
