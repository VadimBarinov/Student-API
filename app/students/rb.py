# Request Body Student
# Описывает тело запроса
class RBStudent:
    # Все параметры необязательные
    # Такая запись эквивалентна Optional[int]
    def __init__(
            self,
            student_id: int | None = None,
            course: int | None = None,
            major_id: int | None = None,
            enrollment_year: int | None = None,
    ):
        self.id = student_id
        self.course = course
        self.major_id = major_id
        self.enrollment_year = enrollment_year

    # Функция для превращения объекта в словарь аргументов
    # Используется при фильтрации запроса в БД
    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "course": self.course,
            "major_id": self.major_id,
            "enrollment_year": self.enrollment_year,
        }
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data