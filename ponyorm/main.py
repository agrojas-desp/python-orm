from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)


class Person(db.Entity):
    name = Required(str)
    age = Required(int)
    cars = Set('Car')


class Car(db.Entity):
    make = Required(str)
    model = Required(str)
    owner = Required(Person)


@db_session
def print_person_name(person_id):
    p = Person[person_id]
    print p.name
    # database session cache will be cleared automatically
    # database connection will be returned to the pool


@db_session
def add_car(person_id, make, model):
    Car(make=make, model=model, owner=Person[person_id])
    # commit() will be done automatically
    # database session cache will be cleared automatically
    # database connection will be returned to the pool


if __name__ == "__main__":
    show(Person)
    p1 = Person(name='John', age=20)
    p2 = Person(name='Mary', age=22)
    p3 = Person(name='Bob', age=30)
    c1 = Car(make='Toyota', model='Prius', owner=p2)
    c2 = Car(make='Ford', model='Explorer', owner=p3)
    commit()
