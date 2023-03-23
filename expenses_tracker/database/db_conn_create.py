from db_schema import db, Tracker


def connect():
    db.connect()


def create_table():
    db.create_tables([Tracker])


def main():
    connect()
    create_table()


if __name__ == '__main__':
    main()
