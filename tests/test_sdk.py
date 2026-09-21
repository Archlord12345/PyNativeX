from __future__ import annotations

import json

import pynativex as pn
from pynativex.cli import main


def test_widget_tree_is_immutable_and_mounts_as_one_batch() -> None:
    row = pn.Row([pn.Text("One"), pn.Text("Two")])
    assert isinstance(row.items, tuple)

    tree = pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("Test")),
        body=pn.Center(pn.Column([pn.Text("Hello"), pn.Button("Continue")], spacing=8)),
    )

    operations = pn.Reconciler().mount(tree)
    encoded = json.loads(pn.Reconciler.encode(operations))

    assert operations[-1].code == pn.OpCode.COMMIT
    assert operations[-1].payload == {"sequence": 1, "version": pn.PROTOCOL_VERSION}
    assert encoded[0]["payload"]["type"] == "Scaffold"
    assert sum(item.code == pn.OpCode.CREATE for item in operations) == 7


def test_reactive_fields_coalesce_dirty_state() -> None:
    class CounterState(pn.State):
        count = pn.field(0)

    state = CounterState()
    assert state.consume_dirty()
    state.count += 1
    state.count += 1
    assert state.count == 2
    assert state.consume_dirty()
    assert not state.consume_dirty()


def test_create_command_generates_runnable_project(tmp_path, capsys) -> None:
    result = main(["--json", "create", "hello-app", "--directory", str(tmp_path)])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["entry"] == "hello_app.main:app"
    assert (tmp_path / "hello-app" / "hello_app" / "main.py").exists()


def test_build_is_explicitly_validation_only(tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert main(["build", "android", "--dry-run"]) == 0
    assert "validated: True" in capsys.readouterr().out
    assert main(["build", "android"]) == 3
    assert "engine artifacts are not published" in capsys.readouterr().out
