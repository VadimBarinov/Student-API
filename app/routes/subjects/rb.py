from typing import Annotated
from fastapi import Depends


class RBSubject:
    def __init__(
            self,
            subject_id: int | None = None,
            subject_name: str | None = None,
    ):
        self.id = subject_id
        self.name = subject_name

    def to_dict(self):
        filtered_data = {
            key: value
            for key, value in {
                "id": self.id,
                "name": self.name,
            }.items() if value is not None
        }
        return filtered_data


RBSubjectDep = Annotated[RBSubject, Depends()]