from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .widgets import Widget

PROTOCOL_VERSION = 1


class OpCode(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    INSERT = "insert"
    SET_HANDLERS = "set_handlers"
    REMOVE = "remove"
    COMMIT = "commit"


@dataclass(frozen=True, slots=True)
class Operation:
    code: OpCode
    node_id: int | None = None
    payload: dict[str, Any] | None = None


class Reconciler:
    """Builds versioned, batched UI operations for the native engine."""

    def __init__(self) -> None:
        self._sequence = 0
        self._next_id = 1

    def mount(self, root: Widget) -> tuple[Operation, ...]:
        operations: list[Operation] = []

        def visit(widget: Widget, parent_id: int | None, index: int) -> None:
            node_id = self._next_id
            self._next_id += 1
            payload = {
                "type": type(widget).__name__,
                "key": widget.key,
                "props": self._serializable_props(widget),
            }
            operations.append(Operation(OpCode.CREATE, node_id, payload))
            handlers = [
                item.name
                for item in widget.__dataclass_fields__.values()
                if item.name != "key" and callable(getattr(widget, item.name))
            ]
            if handlers:
                operations.append(
                    Operation(OpCode.SET_HANDLERS, node_id, {"events": handlers})
                )
            if parent_id is not None:
                operations.append(
                    Operation(OpCode.INSERT, node_id, {"parent": parent_id, "index": index})
                )
            for child_index, child in enumerate(widget.children()):
                visit(child, node_id, child_index)

        visit(root, None, 0)
        self._sequence += 1
        operations.append(
            Operation(
                OpCode.COMMIT,
                payload={"sequence": self._sequence, "version": PROTOCOL_VERSION},
            )
        )
        return tuple(operations)

    @staticmethod
    def encode(operations: tuple[Operation, ...]) -> bytes:
        return json.dumps(
            [asdict(operation) for operation in operations],
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()

    @staticmethod
    def _serializable_props(widget: Widget) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for name, value in widget.props().items():
            if isinstance(value, Widget) or (
                isinstance(value, (list, tuple)) and value and isinstance(value[0], Widget)
            ):
                continue
            if hasattr(value, "__dataclass_fields__"):
                value = asdict(value)
            output[name] = value
        return output
