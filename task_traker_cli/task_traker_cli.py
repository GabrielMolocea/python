import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# File to store tasks
TASKS_FILE = "tasks.json"


def load_tasks() -> List[Dict]:
    """Load tasks from JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read tasks file. Starting fresh.")
            return []
    return []


def save_tasks(tasks: List[Dict]):
    """Save tasks to JSON file."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except IOError:
        print("Error: Could not save tasks.")


def generate_id(tasks: List[Dict]) -> int:
    """Generate a new unique ID for a task."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(tasks: List[Dict], description: str):
    """Add a new task."""
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added with ID: {task['id']}")


def list_tasks(tasks: List[Dict], status_filter: Optional[str] = None):
    """List tasks, optionally filtered by status."""
    filtered = tasks
    if status_filter:
        status_filter = status_filter.lower()
        filtered = [t for t in tasks if t["status"].lower() == status_filter]

    if not filtered:
        print(
            "No tasks found." if not status_filter else f"No tasks with status '{status_filter}'.")
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
        created = task["created_at"][:10]  # YYYY-MM-DD
        emoji = status_emoji.get(task["status"], "❓")
        status_str = f"{emoji} {task['status']}"
        desc = task["description"][:47] + \
            "..." if len(task["description"]) > 47 else task["description"]
        print(f"{task['id']:<4} {status_str:<12} {desc:<50} {created}")
    print("="*80)


def update_status(tasks: List[Dict], task_id: int, new_status: str):
    """Update the status of a task."""
    new_status = new_status.lower()
    valid_statuses = ["todo", "in-progress", "done"]

    if new_status not in valid_statuses:
        print(f"❌ Invalid status. Choose from: {', '.join(valid_statuses)}")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updated_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"✅ Task {task_id} marked as '{new_status}'")
            return
    print(f"❌ Task with ID {task_id} not found.")


def delete_task(tasks: List[Dict], task_id: int):
    """Delete a task."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"🗑️ Task {task_id} deleted.")
            return
    print(f"❌ Task with ID {task_id} not found.")


def show_help():
    """Show available commands."""
    print("\n📋 Task Tracker Commands:")
    print("  add <description>     - Add a new task")
    print("  list                  - List all tasks")
    print("  list todo             - List only todo tasks")
    print("  list in-progress      - List in-progress tasks")
    print("  list done             - List completed tasks")
    print("  mark <id> <status>    - Update task status (todo/in-progress/done)")
    print("  delete <id>           - Delete a task")
    print("  help                  - Show this help")
    print("  quit / exit           - Exit the program")


def main():
    tasks = load_tasks()
    print("🚀 Task Tracker started! Type 'help' for commands.\n")

    while True:
        try:
            command = input("> ").strip()
            if not command:
                continue

            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()

            if cmd in ["quit", "exit"]:
                print("👋 Goodbye!")
                break

            elif cmd == "add":
                if len(parts) < 2:
                    print("❌ Usage: add <task description>")
                else:
                    add_task(tasks, parts[1])

            elif cmd == "list":
                status_filter = parts[1] if len(parts) > 1 else None
                list_tasks(tasks, status_filter)

            elif cmd == "mark":
                if len(parts) < 2:
                    print("❌ Usage: mark <id> <status>")
                    continue
                mark_parts = parts[1].split(maxsplit=1)
                if len(mark_parts) != 2:
                    print("❌ Usage: mark <id> <status>")
                    continue
                try:
                    task_id = int(mark_parts[0])
                    update_status(tasks, task_id, mark_parts[1])
                except ValueError:
                    print("❌ Task ID must be a number.")

            elif cmd == "delete":
                if len(parts) < 2:
                    print("❌ Usage: delete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    delete_task(tasks, task_id)
                except ValueError:
                    print("❌ Task ID must be a number.")

            elif cmd == "help":
                show_help()

            else:
                print(f"❌ Unknown command: {cmd}")
                print("Type 'help' to see available commands.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")


if __name__ == "__main__":
    main()
