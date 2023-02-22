from typing import Any

from src.ast_generator import MyVisitor, MyVisitor2
from src.duplicated_lines_repository import DuplicatedLinesRepository


class DuplicatedLinesFinder:
    @staticmethod
    def find(ast: Any) -> Any:
        generator = MyVisitor(DuplicatedLinesRepository())
        generator.visit(ast)
        return generator.duplicated_lines.list


class DuplicatedLinesRemover:
    @staticmethod
    def find(ast: Any) -> Any:
        generator = MyVisitor2(DuplicatedLinesRepository())
        generator.visit(ast)
        return generator._parallel_ast
