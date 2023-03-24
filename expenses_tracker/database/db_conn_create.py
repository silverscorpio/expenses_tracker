from db_schemas import MerchantTag, Tracker, db


def connect():
    db.connect()


def create_table():
    db.create_tables([Tracker, MerchantTag])


def main():
    connect()
    create_table()


if __name__ == "__main__":
    main()
