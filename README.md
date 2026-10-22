# Project Management CLI Tool

A Python command-line tool for managing users, projects and tasks. Data is saved
locally as JSON in the `data/` folder.

## Features
- Create and list users (name + validated email)
- Add projects to users (one user -> many projects) and list/search them
- Add tasks to projects (one project -> many tasks), assign them to users, mark complete
- Projects show contributors and progress (e.g. `1/2`) from their tasks
- JSON persistence with handling for missing or malformed files
- Pretty tables with `rich`, flexible date parsing with `python-dateutil`

## Project structure
```
main.py            CLI entry point (argparse subcommands)
models/            Person, User, Project, Task, Tracker
utils/helpers.py   JSON load/save helpers
data/              users.json, projects.json, tasks.json
tests/             pytest unit and CLI tests
```

## Setup
Requires Python 3.10+.
```bash
git clone git@github.com:lewismutisya-eng/project_cli.git
cd project_cli
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
(Pipenv also works: `pipenv install --dev`.)

## Usage
```bash
python main.py --help
python main.py add-user --name "Amina" --email "amina@test.com"
python main.py list-users
python main.py add-project --user "Amina" --title "CLI Tool" --description "Python lab" --due-date 2026-11-30
python main.py list-projects --user "Amina"
python main.py search-projects --keyword python
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Amina"
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --title "Implement add-task"
```
Add `--data-dir PATH` before the command to use a different data folder, and `--debug` for logs.

## Tests
```bash
pytest
```

## Known issues
- User and project names must be unique; there are no edit or delete commands yet.
- Not designed for several people writing to the JSON files at once.
