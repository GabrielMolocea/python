import pytest
import os
import json
import tempfile
from datetime import datetime
from task_traker_cli import (
    load_tasks, save_tasks, generate_id, add_task,
    update_status, delete_task, TASKS_FILE
)

# ====================== FIXTURES ======================


@pytest.fixture
def temp_tasks_file():
    """Create a temporary tasks file for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        temp_file = tmp.name

    # Override the TASKS_FILE for testing
    original_file = TASKS_FILE
    globals()["TASKS_FILE"] = temp_file  # Modify the imported constant

    yield temp_file

    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
    globals()["TASKS_FILE"] = original_file  # Restore original


@pytest.fixture
def sample_tasks():
    """Return sample tasks data."""
    return [
        {
            "id": 1,
            "description": "Buy groceries",
            "status": "todo",
            "created_at": "2025-05-22T10:00:00",
            "updated_at": "2025-05-22T10:00:00"
        },
        {
            "id": 2,
            "description": "Finish project report",
            "status": "in-progress",
            "created_at": "2025-05-21T09:30:00",
            "updated_at": "2025-05-22T08:00:00"
        }
    ]


# ====================== TESTS ======================

def test_load_tasks_nonexistent_file(temp_tasks_file):
    tasks = load_tasks()
    assert tasks == []


def test_save_and_load_tasks(temp_tasks_file, sample_tasks):
    save_tasks(sample_tasks)
    loaded = load_tasks()
    assert len(loaded) == 2
    assert loaded[0]["description"] == "Buy groceries"
    assert loaded[1]["status"] == "in-progress"


def test_generate_id_empty_list():
    assert generate_id([]) == 1


def test_generate_id_with_tasks(sample_tasks):
    assert generate_id(sample_tasks) == 3


def test_add_task(temp_tasks_file):
    tasks = []
    add_task(tasks, "Learn Python testing")

    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["description"] == "Learn Python testing"
    assert tasks[0]["status"] == "todo"
    assert "created_at" in tasks[0]
    assert "updated_at" in tasks[0]


def test_update_status_valid(temp_tasks_file, sample_tasks):
    tasks = sample_tasks.copy()
    update_status(tasks, 1, "done")

    assert tasks[0]["status"] == "done"
    assert tasks[0]["updated_at"] > tasks[0]["created_at"]  # Updated timestamp


def test_update_status_invalid_status(temp_tasks_file, sample_tasks, capsys):
    tasks = sample_tasks.copy()
    update_status(tasks, 1, "invalid")

    captured = capsys.readouterr()
    assert "Invalid status" in captured.out
    assert tasks[0]["status"] == "todo"  # Status should not change


def test_update_status_task_not_found(temp_tasks_file, sample_tasks, capsys):
    tasks = sample_tasks.copy()
    update_status(tasks, 999, "done")

    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()


def test_delete_task(temp_tasks_file, sample_tasks):
    tasks = sample_tasks.copy()
    delete_task(tasks, 1)

    assert len(tasks) == 1
    assert tasks[0]["id"] == 2


def test_delete_task_not_found(temp_tasks_file, sample_tasks, capsys):
    tasks = sample_tasks.copy()
    delete_task(tasks, 999)

    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()
    assert len(tasks) == 2  # Should remain unchanged


def test_load_corrupted_file(temp_tasks_file):
    # Create corrupted JSON
    with open(temp_tasks_file, "w") as f:
        f.write("invalid json")

    tasks = load_tasks()
    assert tasks == []  # Should return empty list on error


# ====================== RUN TESTS ======================

if __name__ == "__main__":
    pytest.main(["-v"])
