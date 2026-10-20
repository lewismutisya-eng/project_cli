# Project Management CLI Tool

A basic command-line interface application built in Python to track users, projects, and tasks.

## Setup Instructions
1. Install dependencies:
   pip install -r requirements.txt
2. Run the tests:
   pytest

## Example Commands
- Add a user:
  python main.py add-user --name "Alex" --email "alex@test.com"
- List users:
  python main.py list-users
- Add a project:
  python main.py add-project --user "Alex" --title "CLI Tool" --description "Python lab" --due-date "2026-11-30"
- List projects:
  python main.py list-projects
- Add a task:
  python main.py add-task --project "CLI Tool" --title "Implement code" --assigned-to "Alex"
- Complete a task:
  python main.py complete-task --title "Implement code"
