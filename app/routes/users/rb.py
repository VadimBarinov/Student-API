from typing import Annotated
from fastapi import Depends


class RBUpdateRolesToUser:
    def __init__(
            self,
            user_id: int,
            is_user: bool | None = None,
            is_student: bool | None = None,
            is_teacher: bool | None = None,
            is_admin: bool | None = None,
            is_super_admin: bool | None = None,
    ):
        self.id = user_id
        self.is_user = is_user
        self.is_student = is_student
        self.is_teacher = is_teacher
        self.is_admin = is_admin
        self.is_super_admin = is_super_admin

    def to_dict(self):
        return {
            key: value for key, value in {
                "is_user": self.is_user,
                "is_student": self.is_student,
                "is_teacher": self.is_teacher,
                "is_admin": self.is_admin,
                "is_super_admin": self.is_super_admin,
            }.items() if value is not None
        }

RBUpdateRolesToUserDep = Annotated[RBUpdateRolesToUser, Depends()]