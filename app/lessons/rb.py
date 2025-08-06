class RBLesson:
    def __init__(
            self,
            lesson_id: int | None = None,
            study_group_id: int | None = None,
            teacher_id: int | None = None,
            weekday_id: int | None = None,
            lesson_number: int | None = None,
            auditorium: str | None = None,
    ):
        self.id = lesson_id
        self.study_group_id = study_group_id
        self.teacher_id = teacher_id
        self.weekday_id = weekday_id
        self.lesson_number = lesson_number
        self.auditorium = auditorium

    def to_dict(self):
        filtered_data = {
            key: value for key, value in {
                "id": self.id,
                "study_group_id": self.study_group_id,
                "teacher_id": self.teacher_id,
                "weekday_id": self.weekday_id,
                "lesson_number": self.lesson_number,
                "auditorium": self.auditorium,
            }.items() if value is not None
        }
        return filtered_data