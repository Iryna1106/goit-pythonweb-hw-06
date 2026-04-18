import random
from datetime import date, timedelta

from faker import Faker

from conf.db import DBSession
from conf.models import Grade, Group, Student, Subject, Teacher

NUMBER_STUDENTS = 40
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 4
SUBJECTS_NAMES = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "History",
    "Biology",
    "Literature",
    "Informatics",
]
MAX_GRADES_PER_STUDENT = 20
SEMESTER_START = date(2024, 9, 1)
SEMESTER_END = date(2025, 5, 30)


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def seed() -> None:
    fake = Faker()
    session = DBSession()
    try:
        groups = [Group(name=f"AD-{101 + i}") for i in range(NUMBER_GROUPS)]
        session.add_all(groups)

        teachers = [Teacher(fullname=fake.name()) for _ in range(NUMBER_TEACHERS)]
        session.add_all(teachers)
        session.flush()

        subjects = [
            Subject(name=name, teacher_id=random.choice(teachers).id)
            for name in SUBJECTS_NAMES
        ]
        session.add_all(subjects)

        students = [
            Student(fullname=fake.name(), group_id=random.choice(groups).id)
            for _ in range(NUMBER_STUDENTS)
        ]
        session.add_all(students)
        session.flush()

        for student in students:
            for _ in range(random.randint(10, MAX_GRADES_PER_STUDENT)):
                subject = random.choice(subjects)
                session.add(
                    Grade(
                        student_id=student.id,
                        subject_id=subject.id,
                        grade=random.randint(60, 100),
                        date_of=random_date(SEMESTER_START, SEMESTER_END),
                    )
                )

        session.commit()
        print(
            f"Seeded: {NUMBER_GROUPS} groups, {NUMBER_TEACHERS} teachers, "
            f"{len(SUBJECTS_NAMES)} subjects, {NUMBER_STUDENTS} students."
        )
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


if __name__ == "__main__":
    seed()
