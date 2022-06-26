from typing import Any


class DuplicatedLinesRepository:
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
