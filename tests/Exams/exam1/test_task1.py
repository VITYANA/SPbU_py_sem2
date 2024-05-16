import pytest

from src.Exams.exam1.task1.University import *


class Test_University:
    university = University()
    student1 = Student("Vasya")
    student2 = Student("Oleg")
    teacher1 = Teacher("Maksim Maksim")
    teacher2 = Teacher("Andrey Nikolaevich")
    course1 = Course("Matan")
    course2 = Course("ANT")

    def test_add_stud(self):
        self.university.add_student(self.student1)
        assert self.student1 in self.university.students
        assert len(self.university.students) == 1
        self.university.add_student(self.student2)
        assert self.student2 in self.university.students
        assert len(self.university.students) == 2

    def test_add_teachers(self):
        self.university.add_teacher(self.teacher1)
        assert self.teacher1 in self.university.teachers
        assert len(self.university.teachers) == 1
        self.university.add_teacher(self.teacher2)
        assert self.teacher2 in self.university.teachers
        assert len(self.university.teachers) == 2

    def test_add_courses(self):
        self.university.add_course(self.course1)
        assert self.course1 in self.university.courses
        assert len(self.university.courses) == 1
        self.university.add_course(self.course2)
        assert self.course2 in self.university.courses
        assert len(self.university.courses) == 2

    def test_add_student_to_course(self):
        self.university.add_student_to_course("Vasya", 5, "ANT")
        assert self.student1 in self.course2.students[0].student
        assert len(self.course2.students) == 1
        self.university.add_student_to_course("Oleg", 3, "Matan")
        assert self.student2 in self.course1.students[0].student
        assert len(self.course1.students) == 1
        self.university.add_student_to_course("Vasya", 5, "Matan")
        assert self.student1 in self.course1.students[1].student
        assert len(self.course1.students) == 2

    def test_add_teacher_to_course(self):
        self.university.add_teacher_to_course("Andrey Nikolaevich", "ANT")
        assert self.teacher2 in self.course2.teachers
        assert len(self.course2.teachers) == 1
        self.university.add_teacher_to_course("Maksim Maksim", "Matan")
        assert self.teacher1 in self.course1.teachers
        assert len(self.course1.teachers) == 1
        self.university.add_teacher_to_course("Andrey Nikolaevich", "Matan")
        assert self.teacher2 in self.course1.teachers
        assert len(self.course1.teachers) == 2

    def test_get_student_courses(self):
        assert self.university.get_student_courses("Vasya") == ["ANT", "Matan"]
        assert self.university.get_student_courses("Oleg") == ["Matan"]

    def test_get_student_marks(self):
        assert self.university.get_student_marks("Vasya") == [{"ANT": 5}, {"Matan": 5}]
        assert self.university.get_student_marks("Oleg") == [{"Matan": 3}]

    def test_get_teacher_courses(self):
        assert self.university.get_teacher_courses("Maksim Maksim") == ["Matan"]
        assert self.university.get_teacher_courses("Andrey Nikolaevich") == ["ANT", "Matan"]

    def test_add_student_to_course_miss_student_error(self):
        with pytest.raises(KeyError):
            self.university.add_student_to_course("Miss", 12, "ANT")

    def test_add_student_to_course_miss_course_error(self):
        with pytest.raises(KeyError):
            self.university.add_student_to_course("Oleg", 4, "Geometry")

    def test_add_teacher_to_course_miss_teacher_error(self):
        with pytest.raises(KeyError):
            self.university.add_teacher_to_course("Miss", "ANT")

    def test_add_teacher_to_course_miss_course_error(self):
        with pytest.raises(KeyError):
            self.university.add_teacher_to_course("Andrey Nikolaevich", "Geometry")

    def test_get_student_courses_miss_student_error(self):
        with pytest.raises(KeyError):
            self.university.get_student_courses("Miss")

    def test_get_teacher_courses_miss_teacher_error(self):
        with pytest.raises(KeyError):
            self.university.get_teacher_courses("Miss")

    def test_student_marks_miss_student_error(self):
        with pytest.raises(KeyError):
            self.university.get_student_marks("Miss")
