import pytest
from models.user import User
from models.project import Project

def test_user_creation():
    user = User("Alex", "alex@test.com")
    assert user.name == "Alex"
    assert user.email == "alex@test.com"

def test_invalid_user_email():
    with pytest.raises(ValueError):
        User("Alex", "invalidemail")

def test_project_creation():
    project = Project("CLI Tool", "A great project", "2026-12-31", "Alex")
    assert project.title == "CLI Tool"
    assert project.user_email == "Alex"

def test_empty_project_title():
    with pytest.raises(ValueError):
        Project("", "No title", "2026-12-31", "Alex")
