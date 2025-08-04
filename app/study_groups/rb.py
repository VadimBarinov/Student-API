class RBStudyGroup:
    def __init__(
            self,
            study_group_id: int | None = None,
            study_group_name: str | None = None,
    ):
        self.id = study_group_id
        self.name = study_group_name

    def to_dict(self):
        filtered_data = { key: value for key, value in {
            "id": self.id,
            "name": self.name,
        }.items() if value is not None}
        return filtered_data