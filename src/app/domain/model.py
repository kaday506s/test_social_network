from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str

    first_name: str = None
    last_name: str = None
    middle_name: str = None
    mobile_phone: str = None

    def __str__(self):
        return self.username


@dataclass
class Post:
    id: int
    title: str
    author: str

    text: str
    date_publication: datetime

    def __str__(self):
        return self.title
