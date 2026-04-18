# goit-pythonweb-hw-06

Домашня робота №6 — робота з PostgreSQL через SQLAlchemy, Alembic, Faker.

## Структура

```
.
├── alembic.ini
├── migrations/                 # Alembic (env.py, шаблон, версії)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 2025_01_01_0001_init_schema.py
├── conf/
│   ├── db.py                   # DB URL + engine + DBSession
│   └── models.py               # SQLAlchemy 2.0 моделі
├── seed.py                     # наповнення БД даними через Faker
├── my_select.py                # 10 обов'язкових + 2 додаткових запити
├── main.py                     # CLI (argparse) для CRUD
└── requirements.txt
```

## Схема БД

- `groups` — id, name
- `teachers` — id, fullname
- `students` — id, fullname, group_id → groups
- `subjects` — id, name, teacher_id → teachers
- `grades` — id, student_id → students, subject_id → subjects, grade, date_of

## Підготовка

1. Запустити PostgreSQL у Docker:

   ```bash
   docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
   ```

2. Встановити залежності:

   ```bash
   pip install -r requirements.txt
   ```

3. За потреби перевизначити рядок підключення:

   ```bash
   export DB_URL="postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
   ```

## Міграції (Alembic)

Застосувати міграції:

```bash
alembic upgrade head
```

Згенерувати нову міграцію (після змін у моделях):

```bash
alembic revision --autogenerate -m "message"
```

## Наповнення даними

```bash
python seed.py
```

Створює: 3 групи, 4 викладачів, 7 предметів, 40 студентів, до 20 оцінок на студента.

## Запити

Виконати всі запити:

```bash
python my_select.py
```

Або імпортувати окремі функції `select_1` … `select_12`.

## CLI (CRUD)

```bash
# Створити
python main.py -a create -m Teacher -n 'Boris Jonson'
python main.py -a create -m Group -n 'AD-101'
python main.py -a create -m Student -n 'Jane Doe' --group-id 1
python main.py -a create -m Subject -n 'Math' --teacher-id 1
python main.py -a create -m Grade --student-id 1 --subject-id 1 --grade 90 --date 2024-10-01

# Показати всіх
python main.py -a list -m Teacher

# Оновити
python main.py -a update -m Teacher --id 3 -n 'Andry Bezos'

# Видалити
python main.py -a remove -m Teacher --id 3
```
