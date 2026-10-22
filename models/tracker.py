"""Tracker: loads, links, queries and saves users, projects and tasks."""
import logging
import os

from models.project import Project
from models.task import Task
from models.user import User
from utils.helpers import load_data, save_data

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

logger = logging.getLogger(__name__)


class Tracker:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or DEFAULT_DATA_DIR
        self.users = []
        self.projects = []
        self.tasks = []
        self.load()

    # ---------- persistence ----------
    def _path(self, name):
        return os.path.join(self.data_dir, f"{name}.json")

    def load(self):
        self.users = self._load_items("users", User)
        self.projects = self._load_items("projects", Project)
        self.tasks = self._load_items("tasks", Task)
        self._link()

    def _load_items(self, name, cls):
        items = []
        for record in load_data(self._path(name)):
            try:
                items.append(cls.from_dict(record))
            except (KeyError, TypeError, ValueError) as error:
                logger.warning("Skipping bad %s record %r: %s", name, record, error)
        return items

    def _link(self):
        for project in self.projects:
            owner = self.find_user_by_email(project.owner_email)
            if owner:
                owner.add_project(project)
        for task in self.tasks:
            project = self.find_project_by_id(task.project_id)
            if project:
                project.add_task(task)

    def save(self):
        save_data(self._path("users"), [u.to_dict() for u in self.users])
        save_data(self._path("projects"), [p.to_dict() for p in self.projects])
        save_data(self._path("tasks"), [t.to_dict() for t in self.tasks])

    # ---------- lookups ----------
    def find_user(self, name):
        return next((u for u in self.users if u.name.lower() == name.strip().lower()), None)

    def find_user_by_email(self, email):
        return next((u for u in self.users if u.email == email), None)

    def find_project(self, title):
        return next((p for p in self.projects if p.title.lower() == title.strip().lower()), None)

    def find_project_by_id(self, project_id):
        return next((p for p in self.projects if p.id == project_id), None)

    # ---------- actions ----------
    def add_user(self, name, email):
        user = User(name, email)
        if self.find_user(user.name):
            raise ValueError(f"User '{user.name}' already exists")
        if self.find_user_by_email(user.email):
            raise ValueError(f"Email '{user.email}' is already registered")
        self.users.append(user)
        self.save()
        return user

    def add_project(self, user_name, title, description="", due_date=""):
        owner = self.find_user(user_name)
        if owner is None:
            raise ValueError(f"User '{user_name}' does not exist")
        project = Project(title, description, due_date, owner.email)
        if self.find_project(project.title):
            raise ValueError(f"Project '{project.title}' already exists")
        self.projects.append(project)
        owner.add_project(project)
        self.save()
        return project

    def add_task(self, project_title, title, assigned_to):
        project = self.find_project(project_title)
        if project is None:
            raise ValueError(f"Project '{project_title}' does not exist")
        assignee = self.find_user(assigned_to)
        if assignee is None:
            raise ValueError(f"User '{assigned_to}' does not exist")
        task = Task(title, project.id, assignee.name)
        self.tasks.append(task)
        project.add_task(task)
        self.save()
        return task

    def complete_task(self, title, project_title=None):
        matches = [t for t in self.tasks if t.title.lower() == title.strip().lower()]
        if project_title:
            project = self.find_project(project_title)
            if project is None:
                raise ValueError(f"Project '{project_title}' does not exist")
            matches = [t for t in matches if t.project_id == project.id]
        if not matches:
            raise ValueError(f"Task '{title}' not found")
        if len(matches) > 1:
            raise ValueError(f"More than one task named '{title}'. Add --project to choose.")
        matches[0].complete()
        self.save()
        return matches[0]

    def projects_for_user(self, user_name):
        user = self.find_user(user_name)
        if user is None:
            raise ValueError(f"User '{user_name}' does not exist")
        return list(user.projects)

    def search_projects(self, keyword):
        keyword = keyword.lower()
        return [
            p for p in self.projects
            if keyword in p.title.lower() or keyword in p.description.lower()
        ]

    def tasks_for_project(self, project_title):
        project = self.find_project(project_title)
        if project is None:
            raise ValueError(f"Project '{project_title}' does not exist")
        return list(project.tasks)
