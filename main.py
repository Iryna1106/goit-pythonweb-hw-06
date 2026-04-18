"""CLI for CRUD operations over all models.

Usage examples:
  py main.py -a create -m Teacher -n 'Boris Jonson'
  py main.py -a list   -m Teacher
  py main.py -a update -m Teacher --id 3 -n 'Andry Bezos'
  py main.py -a remove -m Teacher --id 3

  py main.py -a create -m Group   -n 'AD-101'
  py main.py -a create -m Student -n 'Jane Doe' --group-id 1
  py main.py -a create -m Subject -n 'Math'     --teacher-id 1
  py main.py -a create -m Grade   --student-id 1 --subject-id 1 --grade 90 --date 2024-10-01
"""
import argparse
from datetime import datetime

from sqlalchemy import select

from conf.db import DBSession
from conf.models import Grade, Group, Student, Subject, Teacher

MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}


def _parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def _build_payload(model_name: str, args: argparse.Namespace) -> dict:
    if model_name == "Teacher":
        return {"fullname": args.name} if args.name else {}
    if model_name == "Group":
        return {"name": args.name} if args.name else {}
    if model_name == "Student":
        data = {}
        if args.name:
            data["fullname"] = args.name
        if args.group_id is not None:
            data["group_id"] = args.group_id
        return data
    if model_name == "Subject":
        data = {}
        if args.name:
            data["name"] = args.name
        if args.teacher_id is not None:
            data["teacher_id"] = args.teacher_id
        return data
    if model_name == "Grade":
        data = {}
        if args.student_id is not None:
            data["student_id"] = args.student_id
        if args.subject_id is not None:
            data["subject_id"] = args.subject_id
        if args.grade is not None:
            data["grade"] = args.grade
        if args.date:
            data["date_of"] = _parse_date(args.date)
        return data
    raise ValueError(f"Unknown model: {model_name}")


def action_create(session, model, args):
    payload = _build_payload(args.model, args)
    if not payload:
        raise SystemExit("No fields provided for create.")
    obj = model(**payload)
    session.add(obj)
    session.commit()
    print(f"Created: {obj}")


def action_list(session, model, _args):
    rows = session.execute(select(model).order_by(model.id)).scalars().all()
    if not rows:
        print(f"No {model.__name__} records.")
        return
    for row in rows:
        print(row)


def action_update(session, model, args):
    if args.id is None:
        raise SystemExit("--id is required for update.")
    obj = session.get(model, args.id)
    if obj is None:
        raise SystemExit(f"{model.__name__} with id={args.id} not found.")
    payload = _build_payload(args.model, args)
    if not payload:
        raise SystemExit("No fields provided to update.")
    for key, value in payload.items():
        setattr(obj, key, value)
    session.commit()
    print(f"Updated: {obj}")


def action_remove(session, model, args):
    if args.id is None:
        raise SystemExit("--id is required for remove.")
    obj = session.get(model, args.id)
    if obj is None:
        raise SystemExit(f"{model.__name__} with id={args.id} not found.")
    session.delete(obj)
    session.commit()
    print(f"Removed: {model.__name__} id={args.id}")


ACTIONS = {
    "create": action_create,
    "list": action_list,
    "update": action_update,
    "remove": action_remove,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CRUD CLI for university DB")
    parser.add_argument(
        "-a", "--action", required=True, choices=list(ACTIONS.keys()),
        help="CRUD action to perform",
    )
    parser.add_argument(
        "-m", "--model", required=True, choices=list(MODEL_MAP.keys()),
        help="Target model",
    )
    parser.add_argument("--id", type=int, help="Record id (for update/remove)")
    parser.add_argument("-n", "--name", help="Name / fullname field")
    parser.add_argument("--group-id", dest="group_id", type=int)
    parser.add_argument("--teacher-id", dest="teacher_id", type=int)
    parser.add_argument("--student-id", dest="student_id", type=int)
    parser.add_argument("--subject-id", dest="subject_id", type=int)
    parser.add_argument("--grade", type=int, help="Grade value (int)")
    parser.add_argument("--date", help="Grade date YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = MODEL_MAP[args.model]
    handler = ACTIONS[args.action]
    with DBSession() as session:
        handler(session, model, args)


if __name__ == "__main__":
    main()
