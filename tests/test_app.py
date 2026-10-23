import pytest

import main
from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import load_data, save_data


def test_user_creation():
    user = User("Amina", "amina@test.com")
    assert user.name == "Amina"
    assert user.email == "amina@test.com"


def test_user_is_a_person():
    assert isinstance(User("Amina", "amina@test.com"), Person)


def test_invalid_email():
    with pytest.raises(ValueError):
        User("Amina", "invalidemail")


def test_project_creation():
    project = Project("CLI Tool", "A project", "2026-12-31", "Amina")
    assert project.title == "CLI Tool"
    assert project.owner == "Amina"


def test_empty_project_title():
    with pytest.raises(ValueError):
        Project("", "No title", "2026-12-31", "Amina")


def test_bad_due_date():
    with pytest.raises(ValueError):
        Project("CLI Tool", "A project", "tomorrow", "Amina")


def test_task_complete():
    task = Task("Write code", "CLI Tool", "Amina")
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
    save_data(path, [{"name": "Amina"}])
    assert load_data(path) == [{"name": "Amina"}]


def test_cli_full_flow(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    main.main(["add-user", "--name", "Amina", "--email", "amina@test.com"])
    main.main(["add-project", "--user", "Amina", "--title", "CLI Tool"])
    main.main(["add-task", "--project", "CLI Tool", "--title", "Code", "--assigned-to", "Amina"])
    main.main(["complete-task", "--title", "Code"])
    tasks = load_data(str(tmp_path / "tasks.json"))
    assert tasks[0]["status"] == "Complete"


def test_cli_unknown_user(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    main.main(["add-project", "--user", "Nobody", "--title", "X"])
    assert "does not exist" in capsys.readouterr().out
