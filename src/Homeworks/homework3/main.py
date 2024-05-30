import argparse
from base64 import b64decode
from typing import Any

import requests

from src.Homeworks.homework3.Dataclasses import *


def parse_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str)
    parser.add_argument("repository_name", type=str)
    args = parser.parse_args()
    result: tuple[str, str] = (args.username, args.repository_name)
    return result


def write_info() -> str:
    result = (
        "1) Get repository info \n" "2) Get pull request info \n" "3) Get history of commit from branch \n" "4) Exit\n"
    )
    return result


def write_user(user: User) -> str:
    result = f"username: {user.login}\nid: {user.id}\nurl: {user.url}"
    return result


def write_readme(readme: Readme) -> str:
    output_str = "Not found"
    if readme.name:
        readme_data = b64decode(readme.text).decode()
        output_str = f"File name: {readme.name}\n{str(readme_data)}"
        return output_str
    return output_str


def write_repository(repository: Repository, readme: Readme) -> str:
    user_info = write_user(repository.owner)
    readme_info = write_readme(readme)
    result = (
        f"Repo name: {repository.name} \n"
        f"Repository id: {repository.id}\n"
        f"{user_info}\n"
        f"Language: {repository.language}\n"
        f"README.txt: \n"
        f"{readme_info}\n"
    )
    return result


def write_pull_info(pull: Pullrequest) -> str:
    def write_reviewers(requested_reviewers: list[User]) -> str:
        result = ""
        for reviewer in requested_reviewers:
            output_str = f"Reviewer username: {reviewer.login}id: {reviewer.id}\nUrl to profile: {reviewer.url}"
            result += output_str + "\n"
        return result.rstrip("\n")

    owner_info = write_user(pull.owner)
    reviewers_info = write_reviewers(pull.reviewers)
    return (
        f"Pull name: {pull.title} \n"
        f"id: {pull.id}\n"
        f"{owner_info}\n"
        f"Reviewers: \n"
        f"{reviewers_info}\n"
        f"Pull branch: {pull.head.name}\n"
        f"Merging into: {pull.base.name}\n"
    )


def write_pr(pulls: list[Pullrequest]) -> str | None:
    for i, pull in enumerate(pulls):
        print(f"{i}) Pull name: {pull.title}")
    user_choice = input("Choose a pull's number: ")
    try:
        pull_number = int(user_choice)
        return write_pull_info(pulls[pull_number])
    except Exception:
        print("Incorrect number of pull request\n")


def write_commits(branch: Branch) -> str | None:
    last_commit_url = branch.commit.url
    result = ""

    def get_commit_from_url(url: str) -> dict[str, Any]:
        response = requests.get(url)
        return response.json()

    def recursion(current_commit: Commit, result: str) -> str | None:
        if not current_commit.parents:
            return None
        parent = current_commit.parents[0]
        parent_commit = Commit.parse_json(get_commit_from_url(parent.url))
        messages = current_commit.commit.text.split("\n")
        message_text = ""
        recursion(parent_commit, result)
        for message in messages:
            message_text += f"{message}\n"

        result += f"commit:\n{current_commit.id}\n{message_text}"

    json_dict = get_commit_from_url(last_commit_url)
    last_commit_obj = Commit.parse_json(json_dict)
    return recursion(last_commit_obj, result)


def write_branches(branches: list[Branch]) -> str | None:
    for i, branch in enumerate(branches):
        print(f"{i + 1}) Branch name: {branch.name}")
    user_choice = input("Choose a branch number: ")
    try:
        branch_number = int(user_choice) - 1
        result = write_commits(branches[branch_number])
        return result
    except Exception as error:
        print(error)
        print("Incorrect number of branch\n")


def get_repo(username: str, repo_name: str) -> dict[str, Any]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    return repo_response.json()


def get_readme(username: str, repo_name: str) -> dict[str, Any]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md")
    return repo_response.json()


def get_pull_requests(username: str, repo_name: str) -> list[dict[str, Any]]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/pulls")
    return repo_response.json()


def get_branches(username: str, repo_name: str) -> list[dict[str, Any]]:
    repo_response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/branches")
    return repo_response.json()


def main(username: str, repository: str) -> None:
    user_input = ""
    info = write_info()
    print(info)
    while user_input != "4":
        user_input = input("Enter number of request: ")
        if user_input not in "1234":
            print("incorrect number")
            continue
        match user_input:
            case "1":
                repo = Repository.parse_json(get_repo(username, repository))
                readme = Readme.parse_json(get_readme(username, repository))
                print(write_repository(repo, readme))

            case "2":
                pulls = [Pullrequest.parse_json(obj) for obj in get_pull_requests(username, repository)]
                if len(pulls) != 0:
                    print(write_pr(pulls))
                else:
                    print("Can't find any pull requests")

            case "3":
                branches = [Branch.parse_json(obj) for obj in get_branches(username, repository)]
                print(write_branches(branches))
            case "4":
                print("Ending programme")
                break


if __name__ == "__main__":
    main("VITYANA", "SPbU_py_sem2")
