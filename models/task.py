"""Task model: belongs to one Project and is assigned to a user."""

PENDING = "Pending"
COMPLETE = "Complete"
VALID_STATUSES = (PENDING, COMPLETE)


class Task:
    next_id = 1

    def __init__(self, title, project_id, assigned_to, status=PENDING, task_id=None):
        self.title = title
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.status = status
        if task_id is None:
            task_id = Task.next_id
        self.id = task_id
        Task.next_id = max(Task.next_id, task_id + 1)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        self._status = value

    @property
    def is_complete(self):
        return self._status == COMPLETE

    def complete(self):
        self.status = COMPLETE

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["project_id"],
            data["assigned_to"],
            status=data.get("status", PENDING),
            task_id=data.get("id"),
        )

    def __str__(self):
        return f"Task #{self.id}: {self.title} [{self.status}] -> {self.assigned_to}"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
