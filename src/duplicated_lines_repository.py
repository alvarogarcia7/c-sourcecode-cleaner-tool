from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RepeatedVariable:
    name: str
    value: str


# https://roman.pt/posts/dont-let-dicts-spoil-your-code/
@dataclass(frozen=True)
class RepeatedAssignment:
    new: str
    original: str
    variable: RepeatedVariable


class DuplicatedLinesRepository:
    def __init__(self) -> None:
        self._list: list[Any] = []
        self._all_values: set[str] = set()
        self._all_values_with_coord: list[Any] = []
        self._parallel_ast: list[Any] = []

    def register_assignment(self, node: Any, v: Any) -> None:
        values = [int(x.value, 16) for x in v]
        values_str = "".join([str(x) for x in values])
        del v
        if values_str in self._all_values:
            coord = list(filter(lambda x: x['value'] == values_str, self._all_values_with_coord))[0]['coord']
            self._list.append(
                RepeatedAssignment(str(node.coord),
                                   f"{coord.file}:{coord.line}:{coord.column}",
                                   RepeatedVariable(node.name, str(values))))
            return
        self._all_values.add(values_str)
        self._all_values_with_coord.append({'value': values_str, 'coord': node.coord})

    def register_assignment_and_maybe_remove_it(self, node: Any, v: Any) -> bool:
        values = [int(x.value, 16) for x in v]
        values_str = "".join([str(x) for x in values])
        del v
        if values_str in self._all_values:
            coord = list(filter(lambda x: x['value'] == values_str, self._all_values_with_coord))[0]['coord']
            self._list.append(
                RepeatedAssignment(str(node.coord),
                                   f"{coord.file}:{coord.line}:{coord.column}",
                                   RepeatedVariable(node.name, str(values))))
            return False
        self._all_values.add(values_str)
        self._all_values_with_coord.append({'value': values_str, 'coord': node.coord})
        return True

    @property
    def list(self) -> list[Any]:
        return self._list

    def new_ast(self):
        return self._parallel_ast
