import argparse
from tabulate import tabulate
from utils.helpers import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    add_user_parser = subparsers.add_parser("add-user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)

    subparsers.add_parser("list-users")

    add_proj_parser = subparsers.add_parser("add-project")
    add_proj_parser.add_argument("--user", required=True)
    add_proj_parser.add_argument("--title", required=True)
    add_proj_parser.add_argument("--description", default="")
    add_proj_parser.add_argument("--due-date", default="None")

    list_proj_parser = subparsers.add_parser("list-projects")
    list_proj_parser.add_argument("--user", default=None)

    add_task_parser = subparsers.add_parser("add-task")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--assigned-to", required=True)

    complete_task_parser = subparsers.add_parser("complete-task")
    complete_task_parser.add_argument("--title", required=True)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "add-user":
        users = load_data("data/users.json")
        try:
            new_user = User(args.name, args.email)
            users.append({"name": new_user.name, "email": new_user.email})
            save_data("data/users.json", users)
            print(f"Success: Added {new_user}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list-users":
        users = load_data("data/users.json")
        if not users:
            print("No users found.")
        else:
            print(tabulate(users, headers="keys", tablefmt="grid"))

    elif args.command == "add-project":
        users = load_data("data/users.json")
        user_exists = any(u["name"] == args.user for u in users)
        if not user_exists:
            print(f"Error: User '{args.user}' does not exist.")
            return

        projects = load_data("data/projects.json")
        try:
            new_project = Project(args.title, args.description, args.due_date, args.user)
            projects.append({
                "title": new_project.title,
                "description": new_project.description,
                "due_date": new_project.due_date,
                "user_email": new_project.user_email
            })
            save_data("data/projects.json", projects)
            print(f"Success: Created {new_project}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list-projects":
        projects = load_data("data/projects.json")
        if args.user:
            projects = [p for p in projects if p["user_email"] == args.user]
        if not projects:
            print("No projects found.")
        else:
            print(tabulate(projects, headers="keys", tablefmt="grid"))

    elif args.command == "add-task":
        projects = load_data("data/projects.json")
        project_exists = any(p["title"] == args.project for p in projects)
        if not project_exists:
            print(f"Error: Project '{args.project}' does not exist.")
            return

        tasks = load_data("data/tasks.json")
        new_task = Task(args.title, args.project, args.assigned_to)
        tasks.append({
            "title": new_task.title,
            "project_title": new_task.project_title,
            "assigned_to": new_task.assigned_to,
            "status": new_task.status
        })
        save_data("data/tasks.json", tasks)
        print(f"Success: Added {new_task}")

    elif args.command == "complete-task":
        tasks = load_data("data/tasks.json")
        updated = False
        for t in tasks:
            if t["title"] == args.title:
                t["status"] = "Complete"
                updated = True
        if updated:
            save_data("data/tasks.json", tasks)
            print(f"Success: Task '{args.title}' marked as Complete.")
        else:
            print(f"Error: Task '{args.title}' not found.")

if __name__ == "__main__":
    main()
