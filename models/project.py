"""Project model: belongs to one User and owns many Tasks."""
from dateutil import parser as date_parser


def normalize_date(value):
    """Turn a date string such as '2026-11-30' or '30 Nov 2026' into ISO format.

    Returns '' when no date is given. Raises ValueError for bad dates.
    """
    if value is None or str(value).strip() in ("", "None"):
        return ""
    try:
        return date_parser.parse(str(value)).date().isoformat()
    except (ValueError, OverflowError):
        raise ValueError(f"Invalid date: {value!r} (try YYYY-MM-DD)")


class Project:
    next_id = 1

    def __init__(self, title, description, due_date, owner_email, project_id=None):
        self.title = title
        self.description = description or ""
        self.due_date = due_date
        self.owner_email = owner_email
        if project_id is None:
            project_id = Project.next_id
        self.id = project_id
        Project.next_id = max(Project.next_id, project_id + 1)
        self.tasks = []  # one-to-many: Project -> Tasks

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project title cannot be empty")
        self._title = value.strip()

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = normalize_date(value)

    def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)

    @property
    def contributors(self):
        """Everyone with a task on this project (many-to-many via tasks)."""
        return sorted({t.assigned_to for t in self.tasks})

    @property
    def progress(self):
        if not self.tasks:
            return "0/0"
        done = sum(1 for t in self.tasks if t.is_complete)
        return f"{done}/{len(self.tasks)}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_email": self.owner_email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data.get("description", ""),
            data.get("due_date", ""),
            data["owner_email"],
            project_id=data.get("id"),
        )

    def __str__(self):
        due = self.due_date or "no due date"
        return f"Project #{self.id}: {self.title} (due {due}, owner {self.owner_email})"

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title!r})"
