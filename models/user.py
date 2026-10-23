from models.person import Person


class User(Person):
    total_users = 0

    def __init__(self, name, email):
        super().__init__(name)
        self.email = email
        User.total_users += 1

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address")
        self._email = value

    def to_dict(self):
        return {"name": self.name, "email": self.email}

    def __str__(self):
        return f"User: {self.name} ({self.email})"
