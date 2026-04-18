from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from conf.db import DBSession
from conf.models import Grade, Group, Student, Subject, Teacher


def select_1(session: Session):
    """Top-5 students by average grade across all subjects."""
    stmt = (
        select(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(stmt).all()


def select_2(session: Session, subject_id: int):
    """Student with the highest average grade in a given subject."""
    stmt = (
        select(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(stmt).first()


def select_3(session: Session, subject_id: int):
    """Average grade per group for a given subject."""
    stmt = (
        select(
            Group.id,
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(Group.name)
    )
    return session.execute(stmt).all()


def select_4(session: Session):
    """Overall average grade across the whole grades table."""
    stmt = select(func.round(func.avg(Grade.grade), 2))
    return session.execute(stmt).scalar()


def select_5(session: Session, teacher_id: int):
    """List of subjects taught by a given teacher."""
    stmt = select(Subject).where(Subject.teacher_id == teacher_id).order_by(Subject.name)
    return session.execute(stmt).scalars().all()


def select_6(session: Session, group_id: int):
    """List of students in a given group."""
    stmt = (
        select(Student).where(Student.group_id == group_id).order_by(Student.fullname)
    )
    return session.execute(stmt).scalars().all()


def select_7(session: Session, group_id: int, subject_id: int):
    """Grades of students from a given group for a given subject."""
    stmt = (
        select(Student.fullname, Grade.grade, Grade.date_of)
        .join(Grade, Grade.student_id == Student.id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .order_by(Student.fullname, Grade.date_of)
    )
    return session.execute(stmt).all()


def select_8(session: Session, teacher_id: int):
    """Average grade that a given teacher gives across their subjects."""
    stmt = (
        select(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Subject.id == Grade.subject_id)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


def select_9(session: Session, student_id: int):
    """List of courses that a given student attends (has grades in)."""
    stmt = (
        select(Subject)
        .join(Grade, Grade.subject_id == Subject.id)
        .where(Grade.student_id == student_id)
        .distinct()
        .order_by(Subject.name)
    )
    return session.execute(stmt).scalars().all()


def select_10(session: Session, student_id: int, teacher_id: int):
    """Courses a given teacher teaches a given student."""
    stmt = (
        select(Subject)
        .join(Grade, Grade.subject_id == Subject.id)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .order_by(Subject.name)
    )
    return session.execute(stmt).scalars().all()


def select_11(session: Session, student_id: int, teacher_id: int):
    """Average grade that a given teacher gives to a given student."""
    stmt = (
        select(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Subject.id == Grade.subject_id)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


def select_12(session: Session, group_id: int, subject_id: int):
    """Grades of students in a given group for a given subject on the last lesson."""
    last_date_stmt = (
        select(func.max(Grade.date_of))
        .join(Student, Student.id == Grade.student_id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )
    stmt = (
        select(Student.fullname, Grade.grade, Grade.date_of)
        .join(Grade, Grade.student_id == Student.id)
        .where(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_of == last_date_stmt,
        )
        .order_by(Student.fullname)
    )
    return session.execute(stmt).all()


if __name__ == "__main__":
    with DBSession() as session:
        print("1)", select_1(session))
        print("2)", select_2(session, 1))
        print("3)", select_3(session, 1))
        print("4)", select_4(session))
        print("5)", select_5(session, 1))
        print("6)", select_6(session, 1))
        print("7)", select_7(session, 1, 1))
        print("8)", select_8(session, 1))
        print("9)", select_9(session, 1))
        print("10)", select_10(session, 1, 1))
        print("11)", select_11(session, 1, 1))
        print("12)", select_12(session, 1, 1))
