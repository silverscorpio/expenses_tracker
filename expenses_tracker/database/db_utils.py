import peewee

from expenses_tracker.database.db_schemas import TransactionTag


def retrieve_tag(merchant: str) -> int:
    return TransactionTag.get(TransactionTag.merchant_name == merchant).tag


def db_store(database: peewee.SqliteDatabase, model, data: list[dict]):
    with database.atomic():
        model.insert_many(data).execute()


def db_make_table(database: peewee.SqliteDatabase, model: peewee.ModelBase):
    if not database.table_exists(model):
        database.create_tables([model])


if __name__ == "__main__":
    print(retrieve_tag(merchant="no starch press"))
