from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str
    email: str
    name: str
    surname: str