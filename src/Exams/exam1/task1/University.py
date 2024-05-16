class Student:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.courses: list[dict[Course, float]] = []


class Teacher:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.courses: list[Course] = []


class StudentWithMark:
    def __init__(self, student: Student, mark: float) -> None:
        self.student: dict[Student, float] = {student: mark}


class Course:
    def __init__(self, name: str) -> None:
        self.name = name
        self.students: list[StudentWithMark] = []
        self.teachers: list[Teacher] = []


class University:
    def __init__(self) -> None:
        self.students: list[Student] = []
        self.teachers: list[Teacher] = []
        self.courses: list[Course] = []

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def add_teacher(self, teacher: Teacher) -> None:
        self.teachers.append(teacher)

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def _get_student(self, name: str) -> Student | None:
        for student in self.students:
            if name == student.name:
                return student
        return None

    def _get_teacher(self, name: str) -> Teacher | None:
        for teacher in self.teachers:
            if name == teacher.name:
                return teacher
        return None

    def _get_course(self, name: str) -> Course | None:
        for course in self.courses:
            if name == course.name:
                return course
        return None

    def add_student_to_course(self, student_name: str, mark: float, course_name: str) -> None:
        student = self._get_student(student_name)
        if student is None:
            raise KeyError(f"No such student named {student_name} in University.")
        course = self._get_course(course_name)
        if course is None:
            raise KeyError(f"No such course named {course_name} in University.")
        course.students.append(StudentWithMark(student, mark))
        student.courses.append({course: mark})

    def add_teacher_to_course(self, teacher_name: str, course_name: str) -> None:
        teacher = self._get_teacher(teacher_name)
        if teacher is None:
            raise KeyError(f"No such teachers named {teacher_name} in University.")
        course = self._get_course(course_name)
        if course is None:
            raise KeyError(f"No such courses named {course_name} in University.")
        course.teachers.append(teacher)
        teacher.courses.append(course)

    def get_student_courses(self, name: str) -> list[str]:
        student = self._get_student(name)
        if student is None:
            raise KeyError(f"No such student named {name} in University.")
        courses = []
        for course in student.courses:
            for k in course.keys():
                courses.append(k.name)
        return courses

    def get_teacher_courses(self, name: str) -> list[str]:
        teacher = self._get_teacher(name)
        if teacher is None:
            raise KeyError(f"No such teacher named {name} in University.")
        courses = []
        for course in teacher.courses:
            courses.append(course.name)
        return courses

    def get_student_marks(self, name: str) -> list[dict[str, float]]:
        student = self._get_student(name)
        if student is None:
            raise KeyError("No such student in University.")
        marks = []
        for course in student.courses:
            for k, v in course.items():
                marks.append({k.name: v})
        return marks


# university = University()
# student1 = Student("Vasya")
# student2 = Student("Oleg")
# teacher1 = Teacher("Maksim Maksim")
# teacher2 = Teacher("Andrey Nikolaevich")
# course1 = Course("Matan")
# course2 = Course("ANT")
# university.add_student(student1)
# university.add_student(student2)
# university.add_teacher(teacher1)
# university.add_teacher(teacher2)
# university.add_course(course1)
# university.add_course(course2)
# university.add_student_to_course("Vasya", 4, "ANT")
# university.add_student_to_course("Vasya", 5, "Matan")
# print(university.get_student_marks("Vasya"))
# print(university.get_student_courses("Vasya"))
