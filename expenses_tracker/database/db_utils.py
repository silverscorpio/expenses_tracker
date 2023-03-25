import peewee


def db_store(database: peewee.SqliteDatabase, model, data: list[dict]):
    with database.atomic():
        model.insert_many(data).execute()


def db_make_table(database: peewee.SqliteDatabase, model: peewee.ModelBase):
    if not database.table_exists(model):
        database.create_tables([model])


if __name__ == "__main__":
    pass
