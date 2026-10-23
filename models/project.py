from datetime import datetime


class Project:
    def __init__(self, title, description, due_date, owner):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value.strip() == "":
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if value != "":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must look like 2026-11-30")
        self._due_date = value

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner,
        }

    def __str__(self):
        return f"Project: {self.title} (owner: {self.owner}, due: {self.due_date})"
