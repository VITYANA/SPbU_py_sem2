import tempfile

import pytest

from src.Homeworks.homework3.Dataclasses import *
from src.Homeworks.homework3.main import *
from src.Homeworks.homework3.ORM import *


@dataclass
class Person(metaclass=ORM):
    name: str
    surname: str
    age: int


@dataclass
class Worker(metaclass=ORM):
    info: Person
    profession: str


def test_nested():
    cur = Worker.parse_json({"info": {"name": "pip", "surname": "pop", "age": 3}, "profession": "developer"})
    nested = cur.info
    assert isinstance(nested, Person)
    assert nested.name == "pip"
    assert nested.surname == "pop"
    assert nested.age == 3


@pytest.mark.parametrize(
    "orm, data, keys, expected",
    [
        [
            User,
            {"login": "Vitya", "id": 22, "url": "http://pepe"},
            ["login", "id", "url"],
            ["Vitya", 22, "http://pepe"],
        ],
        [Readme, {"name": "read", "text": "me"}, ["name", "text"], ["read", "me"]],
    ],
)
def test_parse_json(orm: ORM, data, keys, expected):
    current = orm.parse_json(data)
    assert [getattr(current, key) for key in keys] == expected


@pytest.mark.parametrize(
    "data,key,expected",
    (
        ({"profession": "economist", "info": {"name": "Albert"}}, "name", "Albert"),
        ({"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}}, "age", 25),
        (
            {"profession": "economist", "info": {"name": "Chu", "surname": "Ling", "age": 27, "nick": "Greedy"}},
            "surname",
            "Ling",
        ),
    ),
)
def test_get_item_branching(data, key, expected):
    current_orm = Worker.parse_json(data)
    assert getattr(current_orm.info, key) == expected


@pytest.mark.parametrize(
    "orm,data,expected",
    (
        (
            User,
            {"login": "Vitya", "id": 22, "url": "http://pepe"},
            {"login": "Vitya", "id": 22, "url": "http://pepe"},
        ),
        (
            User,
            {"login": "arseniy", "id": 12, "url": "http://doge"},
            {"login": "arseniy", "id": 12, "url": "http://doge"},
        ),
        (
            Worker,
            {"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}},
            {"profession": "economist", "info": {"name": "Bob", "surname": "White", "age": 25}},
        ),
    ),
)
def test_dump(orm, data, expected):
    current_orm = orm.parse_json(data)
    with tempfile.NamedTemporaryFile(mode="r+") as file:
        dump_dataclass(current_orm, f"{file.name}")
        assert expected == json.load(file)


@pytest.mark.parametrize(
    "username, repo_name, expected_username, expected_repo_name",
    [
        ("VITYANA", "SPbU_py_sem2", "VITYANA", "SPbU_py_sem2"),
        ("VITYANA", "SPBU_py_sem1", "VITYANA", "SPBU_py_sem1"),
        ("VITYANA", "Lab_work", "VITYANA", "Lab_work"),
    ],
)
def test_get_repo(username, repo_name, expected_username, expected_repo_name):
    repo_dict = get_repo(username, repo_name)
    assert repo_dict["owner"]["login"] == expected_username
    assert repo_dict["name"] == expected_repo_name


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        (
            "VITYANA",
            "SPBU_py_sem1",
            "IyBTUEJVX3B5X3NlbTEKV29ya3MgZnJvbSAxLXN0IHNlbWVzdGVyIGF0IFNQ\nQlUK\n",
        ),
        ("VITYANA", "SPbU_py_sem2", "IyBTUGJVX3B5X3NlbTIKV29ya3MgZnJvbSAyLW5kIHNlbWVzdGVyIGluIFNQ\nYlUuCg==\n"),
        (
            "VITYANA",
            "Lab_work",
            "IyBMYWJfd29yawpsYWJvcmF0b3J5IHdvcmsK\n",
        ),
    ],
)
def test_get_readme(username, repo_name, expected):
    readme_dict = get_readme(username, repo_name)
    assert readme_dict["content"] == expected


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        (
            "VITYANA",
            "SPBU_py_sem1",
            set(),
        ),
        (
            "VITYANA",
            "Lab_work",
            set(),
        ),
    ],
)
def test_get_pull_requests(username, repo_name, expected):
    pulls = get_pull_requests(username, repo_name)
    name_of_pulls = [pull["title"] for pull in pulls]
    assert set(name_of_pulls) == set(expected)


@pytest.mark.parametrize(
    "username, repo_name, expected",
    [
        (
            "VITYANA",
            "SPBU_py_sem1",
            {
                "Test1.task2",
                "file_sort",
                "homework2_task2",
                "homework3",
                "homework4_task2",
                "homework4_task3",
                "homework5_task1",
                "homework5_task2",
                "homework6_task1",
                "main",
                "prac8",
                "prac_7",
                "pract2_task1",
                "pract2_task2",
                "retest2.task2",
                "test2_task1",
                "test2_task2",
            },
        ),
        (
            "VITYANA",
            "Lab_work",
            {"page", "main"},
        ),
    ],
)
def test_get_branches(username, repo_name, expected):
    branches = get_branches(username, repo_name)
    branches_names = [branch["name"] for branch in branches]
    assert set(branches_names) == set(expected)
