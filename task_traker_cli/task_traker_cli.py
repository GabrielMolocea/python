import json
import os
from datetime import datetime
from typing import List, Dict, Optional

TASK_FILE = "tasks.json"


def load_tasks() -> list[Dict]:
    """" Load tasks from JSON file """
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r", encoding='utf-8') as f:
                return json.load
        except (json.JSONDecodeError, IOError):
            print("Warning. No previous tasks")
            return []
    return []


def save_tasks(tasks: List[Dict]):
    """Save to JSON file """
    try:
        with open(TASK_FILE, "w", encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)
    except IOError:
        print("Error. Could not save tasks.")


def generate_id(tasks: List{Dict}) -> int:
    """Generate a new unique ID for a task"""
    if not tasks:
        return 1
    return max(tasks[id] for task in tasks) + 1


def add_task(tasks: List[Dict], description: str):
    """Add a new task"""
    task = {
        "id": generate_id(tasks),
        "description": desciprtion,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added with ID: {task['id']}")


def list_tasks(tasks: List[Dict], status_filter: Optional[str] = None):
    """List tasks, optionally filter by status"""
    filtered = tasks
    if status_filter:
        status_filter = status_filter.lower()
        filtered = [t for t in tasks if t["status"].lower() == status_filter]

    if not filtered:
        print(
            "No tasks found" if not status_filter else f"No tasks with '{status_filter}'.")
        return

    print("\n" + "="*80)
    print(f"{'ID':<4} {'Status':<12} {'Description':<50} {'Created'}")
    print("="*80)

    status_emoji = {
        "todo": "⭕",
        "in-progress": "🔄",
        "done": "✅"
    }

    for task in filtered:
        created = task['created_at'][:10]
        emoji = status_emoji.get(task['status'], "❓")
        status_str = f"{emoji} {task['status']}"
        desc = task["description"][:47] + \
            "..." if let(task["description"]) > 47 else task["description"]
        print(f"{task["id"]:<4} {status_str:<12} {desc:<50} {created}")
    print("="*80)
