from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, Generic, TypeVar, cast

from .widgets import Widget

T = TypeVar("T")


class ReactiveField(Generic[T]):
    def __init__(self, default: T) -> None:
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = f"__pynativex_{name}"

    def __get__(self, instance: State | None, owner: type[State]) -> T | ReactiveField[T]:
        if instance is None:
            return self
        return cast(T, instance.__dict__.get(self.name, self.default))

    def __set__(self, instance: State, value: T) -> None:
        instance.__dict__[self.name] = value
        instance.mark_dirty()


def reactive_field(default: T) -> ReactiveField[T]:
    return ReactiveField(default)


field = reactive_field


class BuildContext:
    def __init__(self, values: dict[type[Any], Any] | None = None) -> None:
        self._values = values or {}

    def provide(self, value: T) -> BuildContext:
        return BuildContext({**self._values, type(value): value})

    def read(self, value_type: type[T]) -> T:
        try:
            return cast(T, self._values[value_type])
        except KeyError as exc:
            raise LookupError(f"No provider registered for {value_type.__name__}") from exc


class State:
    def __init__(self) -> None:
        self._dirty = True
        self._schedule: Callable[[State], None] | None = None

    @property
    def dirty(self) -> bool:
        return self._dirty

    def attach(self, schedule: Callable[[State], None]) -> None:
        self._schedule = schedule

    def mark_dirty(self) -> None:
        if not self._dirty:
            self._dirty = True
            if self._schedule:
                self._schedule(self)

    def consume_dirty(self) -> bool:
        dirty, self._dirty = self._dirty, False
        return dirty

    @contextmanager
    def set_state(self) -> Iterator[None]:
        yield
        self.mark_dirty()

    def init_state(self) -> None:
        pass

    def dispose(self) -> None:
        pass

    def build(self, context: BuildContext) -> Widget:
        raise NotImplementedError


class StatefulWidget(Widget):
    def create_state(self) -> State:
        raise NotImplementedError
