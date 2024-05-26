import pytest

from src.Homeworks.homework3.main import *


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
        ("VITYANA", "SPbU_py_sem2", {"Final_test. Khanukaev Viktor", "Homework2. Khanukaev Viktor"}),
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
            "SPbU_py_sem2",
            {"Final_exam", "Retest1.2", "Test2", "add_changes_for_repo", "homework2", "main", "test1_task1"},
        ),
    ],
)
def test_get_branches(username, repo_name, expected):
    branches = get_branches(username, repo_name)
    branches_names = [branch["name"] for branch in branches]
    assert set(branches_names) == set(expected)
