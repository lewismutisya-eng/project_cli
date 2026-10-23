import pytest

import main
from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import load_data, save_data


def test_user_creation():
    user = User("name", "name@gmail.com")
    assert user.name == "name"
    assert user.email == "name@gmail.com"


def test_user_is_a_person():
    assert isinstance(User("name", "name@gmail.com"), Person)


def test_invalid_email():
    with pytest.raises(ValueError):
        User("name", "invalidemail")


def test_project_creation():
    project = Project("CLI Tool", "A project", "2026-12-31", "name")
    assert project.title == "CLI Tool"
    assert project.owner == "name"


def test_empty_project_title():
    with pytest.raises(ValueError):
        Project("", "No title", "2026-12-31", "name")


def test_bad_due_date():
    with pytest.raises(ValueError):
        Project("CLI Tool", "A project", "tomorrow", "name")


def test_task_complete():
    task = Task("Write code", "CLI Tool", "name")
    assert task.status == "Pending"
    task.complete()
    assert task.status == "Complete"


def test_load_missing_file(tmp_path):
    assert load_data(str(tmp_path / "missing.json")) == []


def test_load_bad_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{this is not json")
    assert load_data(str(bad_file)) == []


def test_save_and_load(tmp_path):
    path = str(tmp_path / "data.json")
    save_data(path, [{"name": "name"}])
    assert load_data(path) == [{"name": "name"}]


def test_cli_full_flow(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    main.main(["add-user", "--name", "name", "--email", "name@gmail.com"])
    main.main(["add-project", "--user", "name", "--title", "CLI Tool"])
    main.main(["add-task", "--project", "CLI Tool", "--title", "Code", "--assigned-to", "name"])
    main.main(["complete-task", "--title", "Code"])
    tasks = load_data(str(tmp_path / "tasks.json"))
    assert tasks[0]["status"] == "Complete"


def test_cli_unknown_user(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    main.main(["add-project", "--user", "Nobody", "--title", "X"])
    assert "does not exist" in capsys.readouterr().out