from typing import Annotated
from fastapi import Depends


class RBStudyGroup:
    def __init__(
            self,
            study_group_id: int | None = None,
            study_group_name: str | None = None,
            count_students: int | None = None,
    ):
        self.id = study_group_id
        self.name = study_group_name
        self.count_students = count_students

    def to_dict(self):
        filtered_data = { key: value for key, value in {
            "id": self.id,
            "name": self.name,
            "count_students": self.count_students,
        }.items() if value is not None}
        return filtered_data


RBStudyGroupDep = Annotated[RBStudyGroup, Depends()]