from __future__ import annotations

import json

import pynativex as pn
import pytest
from gallery_app import PHOTOS, app
from generate_ui import generate


def test_photo_gallery_validates_parallel_metadata() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        pn.PhotoGallery(
            assets=("one", "two"),
            titles=("Only one",),
            captions=("First", "Second"),
        )


def test_gallery_python_ui_compiles_to_android_protocol(tmp_path) -> None:
    output = tmp_path / "gallery_ui.json"

    generate(output)

    document = json.loads(output.read_text(encoding="utf-8"))
    assert document["application"]["title"] == app.title
    gallery_nodes = [
        operation["payload"]
        for operation in document["operations"]
        if operation["code"] == "create"
        and operation["payload"]["type"] == "PhotoGallery"
    ]
    assert len(gallery_nodes) == 1
    assert tuple(gallery_nodes[0]["props"]["assets"]) == PHOTOS
    assert document["operations"][-1]["code"] == "commit"
