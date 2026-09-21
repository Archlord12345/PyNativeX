from __future__ import annotations

import json

import pynativex as pn
from pocket_tasks.main import PocketTasksState, TaskFilter
from pynativex.cli import main


def test_task_state_filters_toggles_and_adds_tasks() -> None:
    state = PocketTasksState()

    assert len(state.visible_tasks()) == 3
    state.set_filter(TaskFilter.ACTIVE)
    assert [task.task_id for task in state.visible_tasks()] == [1, 2]

    state.toggle(1)
    assert [task.task_id for task in state.visible_tasks()] == [2]

    state.add_quick_task()
    assert len(state.tasks) == 4
    assert state.tasks[-1].title == "Nouvelle tâche #4"
    assert state.dirty


def test_app_emits_native_batch_with_interaction_handlers() -> None:
    tree = PocketTasksState().build(pn.BuildContext())
    operations = pn.Reconciler().mount(tree)

    assert operations[-1].code == pn.OpCode.COMMIT
    handlers = [operation for operation in operations if operation.code == pn.OpCode.SET_HANDLERS]
    assert len(handlers) == 7
    assert all(operation.payload == {"events": ["on_press"]} for operation in handlers)


def test_cli_inspects_the_mobile_application(tmp_path, capsys) -> None:
    output = tmp_path / "pocket-tasks-ui.json"

    result = main(
        [
            "inspect",
            "--entry",
            "pocket_tasks.main:app",
            "--output",
            str(output),
        ]
    )

    assert result == 0
    assert capsys.readouterr().out.strip() == str(output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload[0]["type"] == "Scaffold"
    assert payload[-1]["code"] == "commit"
