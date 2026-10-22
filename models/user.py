"""User model: a Person with an email and a list of projects."""
import re

from models.person import Person

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(Person):
    # Class attribute: shared counter used to hand out IDs
    next_id = 1

    def __init__(self, name, email, user_id=None):
        super().__init__(name)
        self.email = email
        if user_id is None:
            user_id = User.next_id
        self.id = user_id
        User.next_id = max(User.next_id, user_id + 1)
        self.projects = []  # one-to-many: User -> Projects

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not EMAIL_PATTERN.match(value.strip()):
            raise ValueError(f"Invalid email address: {value!r}")
        self._email = value.strip().lower()

    def add_project(self, project):
        if project not in self.projects:
            self.projects.append(project)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"], user_id=data.get("id"))

    def __str__(self):
        return f"User #{self.id}: {self.name} ({self.email})"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"
