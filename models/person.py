"""Base class for anything that is a person in the system."""


class Person:
    """A person with a validated name. User inherits from this."""

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"
