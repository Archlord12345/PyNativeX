from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

Callback = Callable[[], None]


@dataclass(frozen=True, slots=True, kw_only=True)
class TextStyle:
    size: float = 14
    weight: int = 400
    color: int = 0xFF111827


@dataclass(frozen=True, slots=True)
class Widget:
    key: str | None = field(default=None, kw_only=True)

    def children(self) -> tuple[Widget, ...]:
        return ()

    def props(self) -> Mapping[str, Any]:
        return {
            item.name: getattr(self, item.name)
            for item in self.__dataclass_fields__.values()
            if item.name != "key" and not callable(getattr(self, item.name))
        }


@dataclass(frozen=True, slots=True)
class Text(Widget):
    value: str
    style: TextStyle = field(default_factory=TextStyle)
    max_lines: int | None = None


@dataclass(frozen=True, slots=True)
class Button(Widget):
    label: str
    on_press: Callback | None = None
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class PhotoGallery(Widget):
    assets: tuple[str, ...]
    titles: tuple[str, ...]
    captions: tuple[str, ...]
    auto_play_seconds: int = 4
    height: float = 420

    def __post_init__(self) -> None:
        item_count = len(self.assets)
        if item_count == 0:
            raise ValueError("PhotoGallery requires at least one photo")
        if len(self.titles) != item_count or len(self.captions) != item_count:
            raise ValueError("PhotoGallery assets, titles and captions must have equal lengths")
        if self.auto_play_seconds < 0:
            raise ValueError("PhotoGallery auto_play_seconds cannot be negative")


@dataclass(frozen=True, slots=True)
class Box(Widget):
    child: Widget | None = None
    color: int | None = None
    padding: float = 0
    radius: float = 0

    def children(self) -> tuple[Widget, ...]:
        return (self.child,) if self.child else ()


@dataclass(frozen=True, slots=True)
class Flex(Widget):
    items: tuple[Widget, ...] = ()
    spacing: float = 0

    def __init__(
        self,
        children: Iterable[Widget] = (),
        *,
        spacing: float = 0,
        key: str | None = None,
    ) -> None:
        object.__setattr__(self, "key", key)
        object.__setattr__(self, "items", tuple(children))
        object.__setattr__(self, "spacing", spacing)

    def children(self) -> tuple[Widget, ...]:
        return self.items


@dataclass(frozen=True, slots=True, init=False)
class Row(Flex):
    pass


@dataclass(frozen=True, slots=True, init=False)
class Column(Flex):
    pass


@dataclass(frozen=True, slots=True)
class Center(Widget):
    child: Widget

    def children(self) -> tuple[Widget, ...]:
        return (self.child,)


@dataclass(frozen=True, slots=True)
class AppBar(Widget):
    title: Widget

    def children(self) -> tuple[Widget, ...]:
        return (self.title,)


@dataclass(frozen=True, slots=True)
class Scaffold(Widget):
    body: Widget
    app_bar: AppBar | None = None

    def children(self) -> tuple[Widget, ...]:
        return ((self.app_bar,) if self.app_bar else ()) + (self.body,)


@dataclass(frozen=True, slots=True)
class App:
    home: Widget
    title: str = "PyNativeX"
