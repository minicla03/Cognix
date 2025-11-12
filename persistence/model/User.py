from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str
    email: str
    name: str
    surname: str

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            data["username"],
            data["password"],
            data["email"],
            data["name"], data["surname"])