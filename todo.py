"""
Simple Command-Line To-Do List Application in Python

This application allows users to manage a simple to-do list from the command line.
Tasks are saved persistently in a local JSON file ('tasks.json').
"""

import json
import os

# Name of the file where tasks are stored
TASKS_FILE = "tasks.json"


def load_tasks(filename=TASKS_FILE):
    """
    Loads tasks from the specified JSON file.
    If the file does not exist or contains invalid JSON, returns an empty list.
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("\nWarning: Could not read tasks file. Starting with an empty list.")
        return []


def save_tasks(tasks, filename=TASKS_FILE):
    """
    Saves the list of tasks to the specified JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"\nError: Could not save tasks to file: {e}")


def list_tasks(tasks):
    """
    Displays all tasks with their 1-based index numbers and completion status.
    Returns True if tasks exist, False if the list is empty.
    """
    if not tasks:
        print("\nYour to-do list is empty!")
        return False
    
    print("\n--- YOUR TO-DO LIST ---")
    for index, item in enumerate(tasks, start=1):
        # Format status indicator: [X] for completed, [ ] for pending
        status = "[X]" if item.get("done", False) else "[ ]"
        task_text = item.get("task", "")
        print(f"{index}. {status} {task_text}")
    print("----------------------")
    return True


def add_task(tasks):
    """
    Prompts the user to enter a new task description and adds it to the list.
    """
    task_text = input("\nEnter the task description: ").strip()
    if not task_text:
        print("Task description cannot be empty!")
        return
    
    # Task stored as a dictionary with 'task' text and 'done' status
    tasks.append({"task": task_text, "done": False})
    save_tasks(tasks)
    print(f'Task "{task_text}" added successfully!')


def mark_task_done(tasks):
    """
    Prompts the user for a task number and marks that task as completed.
    """
    if not list_tasks(tasks):
        return
    
    try:
        task_num = int(input("\nEnter the task number to mark as done: "))
        # Check if the entered task number is valid (1-indexed)
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["done"] = True
            save_tasks(tasks)
            print(f'Task #{task_num} marked as done!')
        else:
            print("Invalid task number. Please select a valid number from the list.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task(tasks):
    """
    Prompts the user for a task number and removes it from the list.
    """
    if not list_tasks(tasks):
        return
    
    try:
        task_num = int(input("\nEnter the task number to delete: "))
        # Check if the entered task number is valid (1-indexed)
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f'Task "{removed_task["task"]}" deleted successfully!')
        else:
            print("Invalid task number. Please select a valid number from the list.")
    except ValueError:
        print("Please enter a valid number.")


def print_menu():
    """
    Displays the main menu options.
    """
    print("\n=========================")
    print("      TO-DO LIST MENU    ")
    print("=========================")
    print("1. List all tasks")
    print("2. Add a task")
    print("3. Mark a task as done")
    print("4. Delete a task")
    print("5. Exit")
    print("=========================")


def main():
    """
    Main loop of the application.
    """
    # Load existing tasks when starting
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("\nGoodbye! Have a productive day!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
