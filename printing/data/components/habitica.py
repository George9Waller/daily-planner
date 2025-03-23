import logging
import os
from datetime import date, datetime, timedelta
from itertools import groupby

import requests

from printing.data.dataclasses import HabiticaTasks
from printing.data.decorators import cached, returns_data_as

logger = logging.getLogger(__name__)


def _transform_checklist(task):
    checklist = task.get("checklist") or []
    return {"checklist": [item["text"] for item in checklist]}


def _transform_habits(habits):
    return habits


def _transform_todos(todos):
    def should_include_todo(todo):
        due_date = todo.get("date")
        if not due_date:
            return True
        return date.today() >= datetime.fromisoformat(due_date).date()

    return [
        todo | _transform_checklist(todo)
        for todo in todos
        if (not todo.get("completed")) and should_include_todo(todo)
    ]


def _transform_dailies(dailies):
    return [
        daily | _transform_checklist(daily)
        for daily in dailies
        if daily.get("isDue") and not daily.get("completed")
    ]


@returns_data_as(HabiticaTasks)
@cached(timedelta(minutes=1))
def get_habitica_tasks(*args, **kwargs):
    def task_type_key(task):
        return task["type"]

    habitica_user_id = os.environ.get("HABITICA_USER_ID")
    habitica_api_token = os.environ.get("HABITICA_API_TOKEN")
    response = requests.get(
        "https://habitica.com/api/v3/tasks/user",
        headers={
            "x-client": f"{habitica_user_id}-daily-planner-project",
            "x-api-user": habitica_user_id,
            "x-api-key": habitica_api_token,
        },
        timeout=30,
    )
    response.raise_for_status()

    sorted_tasks = sorted(response.json()["data"], key=task_type_key)
    tasks_by_type = {
        task_type: list(tasks)
        for task_type, tasks in groupby(sorted_tasks, key=task_type_key)
    }
    return {
        "todos": _transform_todos(tasks_by_type.get("todo", [])),
        "dailies": _transform_dailies(tasks_by_type.get("daily", [])),
        "habits": _transform_habits(tasks_by_type.get("habit", [])),
    }
