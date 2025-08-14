from typing import Annotated
from fastapi import Depends


class RBMajor:
    def __init__(
            self,
            major_id: int | None = None,
            major_name: str | None = None,
            major_description: str | None = None,
            count_students: int | None = None,
    ):
        self.id = major_id
        self.major_name = major_name
        self.major_description = major_description
        self.count_students = count_students

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "major_name": self.major_name,
            "major_description": self.major_description,
            "count_students": self.count_students,
        }
        filtered_data = {
            key: value for key, value in data.items() if value is not None
        }
        return filtered_data


RBMajorDep = Annotated[RBMajor, Depends()]