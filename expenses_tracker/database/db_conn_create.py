from db_schemas import Tracker, TransactionTag, db


def connect():
    db.connect()


def create_table():
    db.create_tables([Tracker, TransactionTag])


def close():
    db.close()


def main():
    connect()
    create_table()
    close()


if __name__ == "__main__":
    main()
