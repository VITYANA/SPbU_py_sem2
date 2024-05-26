from dataclasses import dataclass

from src.Homeworks.homework3.ORM import ORM


@dataclass
class User(metaclass=ORM):
    login: str
    id: int
    url: str


@dataclass
class Repository(metaclass=ORM):
    id: int
    name: str
    owner: User
    language: str


@dataclass
class Readme(metaclass=ORM):
    name: str
    text: str


@dataclass
class Commit(metaclass=ORM):
    @dataclass
    class Message(metaclass=ORM):
        text: str

    @dataclass
    class Parent(metaclass=ORM):
        url: str

    id: str
    commit: Message
    parents: list[Parent]


@dataclass
class Branch(metaclass=ORM):
    @dataclass
    class LastCommit(metaclass=ORM):
        id: str
        url: str

    name: str
    commit: LastCommit


@dataclass
class Pullrequest(metaclass=ORM):
    title: str
    id: int
    owner: User
    reviewers: list[User]
    head: Branch
    base: Branch
