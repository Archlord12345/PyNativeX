from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum

import pynativex as pn


@dataclass(frozen=True, slots=True)
class Task:
    task_id: int
    title: str
    category: str
    done: bool = False


class TaskFilter(StrEnum):
    ALL = "Toutes"
    ACTIVE = "À faire"
    DONE = "Terminées"


class PocketTasksState(pn.State):
    tasks = pn.field(
        (
            Task(1, "Préparer le prototype Android", "PyNativeX"),
            Task(2, "Tester le mode hors-ligne", "Qualité"),
            Task(3, "Inviter un contributeur", "Communauté", done=True),
        )
    )
    selected_filter = pn.field(TaskFilter.ALL)

    def set_filter(self, selected: TaskFilter) -> None:
        self.selected_filter = selected

    def toggle(self, task_id: int) -> None:
        self.tasks = tuple(
            replace(task, done=not task.done) if task.task_id == task_id else task
            for task in self.tasks
        )

    def add_quick_task(self) -> None:
        next_id = max((task.task_id for task in self.tasks), default=0) + 1
        self.tasks = (
            *self.tasks,
            Task(next_id, f"Nouvelle tâche #{next_id}", "Personnel"),
        )

    def visible_tasks(self) -> tuple[Task, ...]:
        if self.selected_filter == TaskFilter.ACTIVE:
            return tuple(task for task in self.tasks if not task.done)
        if self.selected_filter == TaskFilter.DONE:
            return tuple(task for task in self.tasks if task.done)
        return self.tasks

    def _filter_button(self, task_filter: TaskFilter) -> pn.Widget:
        selected = self.selected_filter == task_filter
        return pn.Box(
            pn.Button(
                task_filter.value,
                on_press=lambda selected_filter=task_filter: self.set_filter(selected_filter),
            ),
            color=0xFF0369A1 if selected else 0xFFE0F2FE,
            padding=4,
            radius=12,
        )

    def _task_card(self, task: Task) -> pn.Widget:
        status = "Terminée" if task.done else "À faire"
        status_color = 0xFF15803D if task.done else 0xFFB45309
        return pn.Box(
            pn.Row(
                [
                    pn.Column(
                        [
                            pn.Text(
                                task.title,
                                style=pn.TextStyle(
                                    size=17,
                                    weight=600,
                                    color=0xFF64748B if task.done else 0xFF0F172A,
                                ),
                            ),
                            pn.Text(
                                f"{task.category} · {status}",
                                style=pn.TextStyle(size=13, color=status_color),
                            ),
                        ],
                        spacing=5,
                    ),
                    pn.Button(
                        "Rouvrir" if task.done else "Terminer",
                        on_press=lambda task_id=task.task_id: self.toggle(task_id),
                    ),
                ],
                spacing=12,
            ),
            color=0xFFF8FAFC,
            padding=16,
            radius=16,
            key=f"task-{task.task_id}",
        )

    def build(self, context: pn.BuildContext) -> pn.Widget:
        completed = sum(task.done for task in self.tasks)
        total = len(self.tasks)
        visible = self.visible_tasks()
        cards = (
            [self._task_card(task) for task in visible]
            if visible
            else [
                pn.Box(
                    pn.Center(pn.Text("Aucune tâche dans cette catégorie.")),
                    color=0xFFF1F5F9,
                    padding=24,
                    radius=16,
                )
            ]
        )

        return pn.Scaffold(
            app_bar=pn.AppBar(pn.Text("Pocket Tasks")),
            body=pn.Column(
                [
                    pn.Text(
                        "Ma journée",
                        style=pn.TextStyle(size=30, weight=700, color=0xFF0C4A6E),
                    ),
                    pn.Text(
                        f"{completed} tâche(s) terminée(s) sur {total}",
                        style=pn.TextStyle(size=15, color=0xFF475569),
                    ),
                    pn.Row(
                        [self._filter_button(task_filter) for task_filter in TaskFilter],
                        spacing=8,
                    ),
                    *cards,
                    pn.Button("Ajouter une tâche rapide", on_press=self.add_quick_task),
                ],
                spacing=12,
            ),
        )


state = PocketTasksState()
app = pn.App(
    title="Pocket Tasks",
    home=state.build(pn.BuildContext()),
)
