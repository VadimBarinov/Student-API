import requests


def get_all_students_with_param(
        course: int,
        major: str,
        enrollment_year: int
):
    url = f"http://127.0.0.1:8000/students/{course}"
    response = requests.get(url, params={
        "course": course,
        "major": major,
        "enrollment_year": enrollment_year,
    })
    return response.json()


def get_student_from_id(student_id: int):
    url = f"http://127.0.0.1:8000/student/{student_id}"
    response = requests.get(url, params={
        "student_id": student_id,
    })
    return response.json()


def get_student_from_param_id(student_id: int):
    url = f"http://127.0.0.1:8000/student"
    response = requests.get(url, params={
        "student_id": student_id,
    })
    return response.json()


course = 2
print(f"\nTest /students/{course} (GET): ")
students = get_all_students_with_param(course=2, major=None, enrollment_year=2018)
for student in students:
    print(student)
print("-----------------------------------------------------------------------------")


student_id = 2
print(f"\nTest /student/{student_id} (GET): ")
student = get_student_from_id(student_id=2)
print(student)
print("-----------------------------------------------------------------------------")


student_id = 5
print(f"\nTest /student/?student_id={student_id} (GET): ")
student = get_student_from_param_id(student_id=5)
print(student)
print("-----------------------------------------------------------------------------")