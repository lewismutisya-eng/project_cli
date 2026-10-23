import argparse
import os

from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import load_data, save_data

console = Console()

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def file_path(name):
    return os.path.join(DATA_DIR, name)


def print_table(title, columns, rows):
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def add_user(args):
    users = load_data(file_path("users.json"))
    for u in users:
        if u["name"].lower() == args.name.lower():
            print(f"Error: User '{args.name}' already exists.")
            return
    try:
        user = User(args.name, args.email)
    except ValueError as error:
        print(f"Error: {error}")
        return
    users.append(user.to_dict())
    save_data(file_path("users.json"), users)
    print(f"Success: Added {user}")


def list_users(args):
    users = load_data(file_path("users.json"))
    if len(users) == 0:
        print("No users found.")
        return
    rows = [[u["name"], u["email"]] for u in users]
    print_table("Users", ["Name", "Email"], rows)


def add_project(args):
    users = load_data(file_path("users.json"))
    owner = None
    for u in users:
        if u["name"].lower() == args.user.lower():
            owner = u["name"]
    if owner is None:
        print(f"Error: User '{args.user}' does not exist.")
        return

    projects = load_data(file_path("projects.json"))
    for p in projects:
        if p["title"].lower() == args.title.lower():
            print(f"Error: Project '{args.title}' already exists.")
            return
    try:
        project = Project(args.title, args.description, args.due_date, owner)
    except ValueError as error:
        print(f"Error: {error}")
        return
    projects.append(project.to_dict())
    save_data(file_path("projects.json"), projects)
    print(f"Success: Added {project}")


def list_projects(args):
    projects = load_data(file_path("projects.json"))
    if args.user:
        projects = [p for p in projects if p["owner"].lower() == args.user.lower()]
    if len(projects) == 0:
        print("No projects found.")
        return
    rows = [[p["title"], p["description"], p["due_date"], p["owner"]] for p in projects]
    print_table("Projects", ["Title", "Description", "Due date", "Owner"], rows)


def search_projects(args):
    projects = load_data(file_path("projects.json"))
    word = args.keyword.lower()
    found = []
    for p in projects:
        if word in p["title"].lower() or word in p["description"].lower():
            found.append(p)
    if len(found) == 0:
        print("No projects found.")
        return
    rows = [[p["title"], p["description"], p["due_date"], p["owner"]] for p in found]
    print_table("Search results", ["Title", "Description", "Due date", "Owner"], rows)


def add_task(args):
    projects = load_data(file_path("projects.json"))
    project_title = None
    for p in projects:
        if p["title"].lower() == args.project.lower():
            project_title = p["title"]
    if project_title is None:
        print(f"Error: Project '{args.project}' does not exist.")
        return

    users = load_data(file_path("users.json"))
    assignee = None
    for u in users:
        if u["name"].lower() == args.assigned_to.lower():
            assignee = u["name"]
    if assignee is None:
        print(f"Error: User '{args.assigned_to}' does not exist.")
        return

    try:
        task = Task(args.title, project_title, assignee)
    except ValueError as error:
        print(f"Error: {error}")
        return
    tasks = load_data(file_path("tasks.json"))
    tasks.append(task.to_dict())
    save_data(file_path("tasks.json"), tasks)
    print(f"Success: Added {task}")


def list_tasks(args):
    tasks = load_data(file_path("tasks.json"))
    tasks = [t for t in tasks if t["project"].lower() == args.project.lower()]
    if len(tasks) == 0:
        print("No tasks found.")
        return
    rows = [[t["title"], t["assigned_to"], t["status"]] for t in tasks]
    print_table(f"Tasks in {args.project}", ["Title", "Assigned to", "Status"], rows)


def complete_task(args):
    tasks = load_data(file_path("tasks.json"))
    for t in tasks:
        if t["title"].lower() == args.title.lower():
            t["status"] = "Complete"
            save_data(file_path("tasks.json"), tasks)
            print(f"Success: Task '{t['title']}' marked as Complete.")
            return
    print(f"Error: Task '{args.title}' not found.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    p = subparsers.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True, help="Name of the user")
    p.add_argument("--email", required=True, help="Email of the user")
    p.set_defaults(func=add_user)

    p = subparsers.add_parser("list-users", help="Show all users")
    p.set_defaults(func=list_users)

    p = subparsers.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True, help="Name of the owner")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--description", default="", help="Project description")
    p.add_argument("--due-date", default="", help="Due date like 2026-11-30")
    p.set_defaults(func=add_project)

    p = subparsers.add_parser("list-projects", help="Show projects (all, or one user's)")
    p.add_argument("--user", default=None, help="Only show this user's projects")
    p.set_defaults(func=list_projects)

    p = subparsers.add_parser("search-projects", help="Search projects by keyword")
    p.add_argument("--keyword", required=True, help="Word to look for")
    p.set_defaults(func=search_projects)

    p = subparsers.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--assigned-to", required=True, help="Name of the user")
    p.set_defaults(func=add_task)

    p = subparsers.add_parser("list-tasks", help="Show the tasks of a project")
    p.add_argument("--project", required=True, help="Project title")
    p.set_defaults(func=list_tasks)

    p = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--title", required=True, help="Task title")
    p.set_defaults(func=complete_task)

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
