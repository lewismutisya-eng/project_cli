import json

import pytest

from main import main
from models.person import Person
from models.project import Project, normalize_date
from models.task import Task
from models.tracker import Tracker
from models.user import User
from utils.helpers import load_data, save_data


@pytest.fixture
def tracker(tmp_path):
    return Tracker(str(tmp_path))


# ---------- models ----------
def test_user_inherits_person():
    user = User("Amina", "Amina@Test.com")
    assert isinstance(user, Person)
    assert user.email == "amina@test.com"


@pytest.mark.parametrize("bad", ["invalidemail", "a@b", "", "a b@c.com"])
def test_invalid_email(bad):
    with pytest.raises(ValueError):
        User("Amina", bad)


def test_empty_name_rejected():
    with pytest.raises(ValueError):
        User("  ", "a@b.com")


def test_project_validation():
    assert Project("CLI", "d", "2026-11-30", "a@b.com").due_date == "2026-11-30"
    with pytest.raises(ValueError):
        Project("", "d", "2026-11-30", "a@b.com")
    with pytest.raises(ValueError):
        Project("CLI", "d", "not-a-date", "a@b.com")


def test_normalize_date_formats():
    assert normalize_date("30 Nov 2026") == "2026-11-30"
    assert normalize_date("") == ""


def test_task_status_property():
    task = Task("Code", 1, "Amina")
    assert task.status == "Pending"
    task.complete()
    assert task.is_complete
    with pytest.raises(ValueError):
        task.status = "Nonsense"


# ---------- tracker / relationships ----------
def test_full_flow_and_relationships(tracker):
    tracker.add_user("Amina", "amina@test.com")
    tracker.add_user("Sam", "sam@test.com")
    project = tracker.add_project("Amina", "CLI Tool", "Python lab", "2026-11-30")
    tracker.add_task("CLI Tool", "Write code", "Amina")
    tracker.add_task("CLI Tool", "Review code", "Sam")
    assert len(tracker.find_user("Amina").projects) == 1
    assert project.contributors == ["Amina", "Sam"]
    assert project.progress == "0/2"
    tracker.complete_task("Write code")
    assert project.progress == "1/2"


def test_duplicates_and_missing_refs(tracker):
    tracker.add_user("Amina", "amina@test.com")
    with pytest.raises(ValueError):
        tracker.add_user("Amina", "other@test.com")
    with pytest.raises(ValueError):
        tracker.add_user("Wanjiru", "amina@test.com")
    with pytest.raises(ValueError):
        tracker.add_project("Ghost", "P")
    with pytest.raises(ValueError):
        tracker.add_task("Nope", "T", "Amina")
    with pytest.raises(ValueError):
        tracker.complete_task("Nothing")


def test_search_projects(tracker):
    tracker.add_user("Amina", "amina@test.com")
    tracker.add_project("Amina", "CLI Tool", "Python lab")
    tracker.add_project("Amina", "Website", "landing page")
    assert [p.title for p in tracker.search_projects("python")] == ["CLI Tool"]


def test_data_persists_between_runs(tmp_path):
    first = Tracker(str(tmp_path))
    first.add_user("Amina", "amina@test.com")
    first.add_project("Amina", "CLI Tool")
    first.add_task("CLI Tool", "Code", "Amina")
    second = Tracker(str(tmp_path))
    assert second.find_project("CLI Tool").tasks[0].title == "Code"
    assert second.find_user("Amina").projects[0].title == "CLI Tool"


# ---------- file I/O ----------
def test_load_missing_and_malformed(tmp_path):
    assert load_data(str(tmp_path / "nope.json")) == []
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert load_data(str(bad)) == []
    notlist = tmp_path / "obj.json"
    notlist.write_text(json.dumps({"a": 1}))
    assert load_data(str(notlist)) == []


def test_save_creates_folder(tmp_path):
    target = tmp_path / "new" / "x.json"
    save_data(str(target), [{"a": 1}])
    assert load_data(str(target)) == [{"a": 1}]


# ---------- CLI ----------
def test_cli_end_to_end(tmp_path, capsys):
    d = ["--data-dir", str(tmp_path)]
    assert main(d + ["add-user", "--name", "Amina", "--email", "amina@test.com"]) == 0
    assert main(d + ["add-project", "--user", "Amina", "--title", "CLI Tool"]) == 0
    assert main(d + ["add-task", "--project", "CLI Tool", "--title", "Code", "--assigned-to", "Amina"]) == 0
    assert main(d + ["complete-task", "--title", "Code"]) == 0
    assert main(d + ["list-projects", "--user", "Amina"]) == 0
    assert "CLI Tool" in capsys.readouterr().out


def test_cli_errors_return_1(tmp_path):
    d = ["--data-dir", str(tmp_path)]
    assert main(d + ["add-project", "--user", "Ghost", "--title", "X"]) == 1
    assert main(d + ["add-user", "--name", "A", "--email", "bad"]) == 1


def test_cli_no_command_prints_help(capsys):
    assert main([]) == 0
    assert "usage" in capsys.readouterr().out.lower()
