from SQLAlchemy.sqlalchemy_declarative import run_create
from SQLAlchemy.sqlalchemy_insert import run_insert
from SQLAlchemy.sqlalchemy_select import run_select

if __name__ == '__main__':
    run_create()
    run_insert()
    run_select()