import argparse
from tabulate import tabulate
from utils.helpers import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

USERS_FILE = "data/users.json"
PROJECTS_FILE = "data/projects.json"
TASKS_FILE = "data/tasks.json"

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-users")
    p_add_user = subparsers.add_parser("add-user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=True)

    p_add_proj = subparsers.add_parser("add-project")
    p_add_proj.add_argument("--user", required=True)
    p_add_proj.add_argument("--title", required=True)

    p_list_proj = subparsers.add_parser("list-projects")
    p_list_proj.add_argument("--user", default=None)

    p_add_task = subparsers.add_parser("add-task")
    p_add_task.add_argument("--project", required=True)
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assigned-to", required=True)

    p_comp_task = subparsers.add_parser("complete-task")
    p_comp_task.add_argument("--title", required=True)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    if args.command == "add-user":
        users = load_data(USERS_FILE)
        try:
            new_user = User(args.name, args.email)
            users.append({"name": new_user.name, "email": new_user.email})
            save_data(USERS_FILE, users)
            print(f"Success: Added {new_user}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list-users":
        users = load_data(USERS_FILE)
        print(tabulate(users, headers="keys", tablefmt="grid") if users else "No users found.")

    elif args.command == "add-project":
        users = load_data(USERS_FILE)
        if not any(u["name"] == args.user for u in users):
            print(f"Error: User '{args.user}' does not exist.")
            return
        projects = load_data(PROJECTS_FILE)
        try:
            new_project = Project(args.title, "No description", "None", args.user)
            projects.append({"title": new_project.title, "user_email": new_project.user_email})
            save_data(PROJECTS_FILE, projects)
            print(f"Success: Created {new_project}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list-projects":
        projects = load_data(PROJECTS_FILE)
        if args.user:
            projects = [p for p in projects if p["user_email"] == args.user]
        print(tabulate(projects, headers="keys", tablefmt="grid") if projects else "No projects found.")

    elif args.command == "add-task":
        projects = load_data(PROJECTS_FILE)
        if not any(p["title"] == args.project for p in projects):
            print(f"Error: Project '{args.project}' does not exist.")
            return
        tasks = load_data(TASKS_FILE)
        new_task = Task(args.title, args.project, args.assigned_to)
        tasks.append({"title": new_task.title, "project_title": new_task.project_title, "assigned_to": new_task.assigned_to, "status": new_task.status})
        save_data(TASKS_FILE, tasks)
        print(f"Success: Added {new_task}")

    elif args.command == "complete-task":
        tasks = load_data(TASKS_FILE)
        updated = False
        for t in tasks:
            if t["title"] == args.title:
                t["status"] = "Complete"
                updated = True
        if updated:
            save_data(TASKS_FILE, tasks)
            print(f"Success: Task '{args.title}' marked as Complete.")
        else:
            print(f"Error: Task '{args.title}' not found.")

if __name__ == "__main__":
    main()
