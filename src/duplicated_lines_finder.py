from typing import Any

from src.duplicated_lines_repository import DuplicatedLinesRepository
from src.ast_generator import MyVisitor


class DuplicatedLinesFinder:
    @staticmethod
    def find(ast: Any) -> Any:
        generator = MyVisitor(DuplicatedLinesRepository())
        generator.visit(ast)
        return generator.duplicated_lines.list
