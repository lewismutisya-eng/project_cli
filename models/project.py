class Project:
    def __init__(self, title, description, due_date, user_email):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_email = user_email

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        self._title = value

    def __str__(self):
        return f"Project: {self.title} | Due: {self.due_date} | Assigned to: {self.user_email}"
