"""Project Management CLI Tool - entry point."""
import argparse
import logging
import sys

from rich.console import Console
from rich.table import Table

from models.tracker import Tracker

console = Console()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Project Management CLI Tool: manage users, projects and tasks.",
    )
    parser.add_argument("--data-dir", default=None, help="Folder for the JSON data files (default: ./data)")
    parser.add_argument("--debug", action="store_true", help="Show debug logging")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p = sub.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True, help="User's name")
    p.add_argument("--email", required=True, help="User's email")

    sub.add_parser("list-users", help="List all users")

    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True, help="Name of the owner")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--description", default="", help="Project description")
    p.add_argument("--due-date", default="", help="Due date, e.g. 2026-11-30")

    p = sub.add_parser("list-projects", help="List projects (optionally for one user)")
    p.add_argument("--user", default=None, help="Only show this user's projects")

    p = sub.add_parser("search-projects", help="Search projects by keyword")
    p.add_argument("--keyword", required=True, help="Text to look for in title or description")

    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--assigned-to", required=True, help="Name of the assignee")

    p = sub.add_parser("list-tasks", help="List tasks of a project")
    p.add_argument("--project", required=True, help="Project title")

    p = sub.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--project", default=None, help="Project title (needed if titles repeat)")
    return parser


def show_table(title, columns, rows):
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    console.print(table)


def run(args, tracker):
    cmd = args.command
    if cmd == "add-user":
        user = tracker.add_user(args.name, args.email)
        console.print(f"[green]Success:[/green] Added {user}")
    elif cmd == "list-users":
        if not tracker.users:
            console.print("No users found.")
        else:
            show_table("Users", ["ID", "Name", "Email", "Projects"],
                       [(u.id, u.name, u.email, len(u.projects)) for u in tracker.users])
    elif cmd == "add-project":
        project = tracker.add_project(args.user, args.title, args.description, args.due_date)
        console.print(f"[green]Success:[/green] Created {project}")
    elif cmd in ("list-projects", "search-projects"):
        if cmd == "search-projects":
            projects = tracker.search_projects(args.keyword)
        elif args.user:
            projects = tracker.projects_for_user(args.user)
        else:
            projects = tracker.projects
        if not projects:
            console.print("No projects found.")
        else:
            show_table("Projects", ["ID", "Title", "Description", "Due", "Owner", "Done"],
                       [(p.id, p.title, p.description, p.due_date, p.owner_email, p.progress)
                        for p in projects])
    elif cmd == "add-task":
        task = tracker.add_task(args.project, args.title, args.assigned_to)
        console.print(f"[green]Success:[/green] Added {task}")
    elif cmd == "list-tasks":
        tasks = tracker.tasks_for_project(args.project)
        if not tasks:
            console.print("No tasks found.")
        else:
            show_table(f"Tasks in {args.project}", ["ID", "Title", "Assigned to", "Status"],
                       [(t.id, t.title, t.assigned_to, t.status) for t in tasks])
    elif cmd == "complete-task":
        task = tracker.complete_task(args.title, args.project)
        console.print(f"[green]Success:[/green] Task '{task.title}' marked as Complete.")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        run(args, Tracker(args.data_dir))
    except ValueError as error:
        console.print(f"[red]Error:[/red] {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
