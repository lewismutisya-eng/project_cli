class Task:
    def __init__(self, title, project, assigned_to, status="Pending"):
        self.title = title
        self.project = project
        self.assigned_to = assigned_to
        self.status = status

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value.strip() == "":
            raise ValueError("Task title cannot be empty")
        self._title = value

    def complete(self):
        self.status = "Complete"

    def to_dict(self):
        return {
            "title": self.title,
            "project": self.project,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    def __str__(self):
        return f"Task: {self.title} [{self.status}] assigned to {self.assigned_to}"
