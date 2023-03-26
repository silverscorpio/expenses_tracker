import peewee

from expenses_tracker.database.db_schemas import TransactionTag


def if_merchant_exists(merchant: str) -> bool:
    return (
        TransactionTag.select().where(TransactionTag.merchant_name == merchant).exists()
    )


def retrieve_tag(merchant: str) -> int:
    return TransactionTag.get(TransactionTag.merchant_name == merchant).tag


def db_store(database: peewee.SqliteDatabase, model, data: list[dict]):
    try:
        with database.atomic():
            model.insert_many(data).execute()
    except peewee.IntegrityError:
        print("duplicate transaction")


def db_make_table(database: peewee.SqliteDatabase, model: peewee.ModelBase):
    if not database.table_exists(model):
        database.create_tables([model])


if __name__ == "__main__":
    pass
