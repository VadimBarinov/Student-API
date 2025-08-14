from typing import Annotated
from fastapi import Depends


class RBTeacher:
    def __init__(
            self,
            teacher_id: int | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            patronymic: str | None = None,
            major_id: int | None = None,
    ):
        self.id = teacher_id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.major_id = major_id

    def to_dict(self):
        filtered_data = {
            key: value for key, value in {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "patronymic": self.patronymic,
                "major_id": self.major_id,
            }.items() if value is not None
        }
        return filtered_data


RBTeacherDep = Annotated[RBTeacher, Depends()]