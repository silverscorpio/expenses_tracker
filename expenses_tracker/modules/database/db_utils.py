import peewee

from .db_schemas import TransactionTag


def if_merchant_exists(merchant: str) -> bool:
    return (
        TransactionTag.select().where(TransactionTag.merchant_name == merchant).exists()
    )


def retrieve_tag(merchant: str) -> int:
    if if_merchant_exists(merchant=merchant):
        return TransactionTag.get(TransactionTag.merchant_name == merchant).tag
    return 6  # uploaded (guaranteed no merchant)


def db_store(
    database: peewee.SqliteDatabase, model, data: list[dict], loop_over: bool = False
):
    if loop_over:
        for transaction in data:
            try:
                with database.atomic():
                    model.create(**transaction)
            except peewee.IntegrityError:
                print(f"duplicate transaction - {transaction}")
                continue
    else:
        try:
            with database.atomic():
                model.insert_many(data).execute()
        except peewee.IntegrityError:
            print("duplicate transaction")


def db_store_single(database: peewee.SqliteDatabase, model, **kwargs):
    try:
        with database.atomic():
            model.create(**kwargs)
    except peewee.IntegrityError:
        print("duplicate transaction")


def db_make_table(database: peewee.SqliteDatabase, model: peewee.ModelBase):
    if not database.table_exists(model):
        database.create_tables([model])


if __name__ == "__main__":
    print(retrieve_tag(merchant=""))
