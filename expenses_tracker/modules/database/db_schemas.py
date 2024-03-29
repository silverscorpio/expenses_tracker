import peewee
from peewee import *

from ..settings import DATABASE_PATH


def get_db(db_path: str) -> peewee.SqliteDatabase:
    return SqliteDatabase(db_path)


db = get_db(db_path=DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Expenses(BaseModel):
    merchant = CharField()
    money_spent = FloatField()
    current_balance = FloatField()
    money_added = FloatField()
    transaction_date_ger = DateField()
    transaction_time_ger = TimeField()
    old_balance = FloatField()
    tag = CharField()
    transaction_date_ind = DateField()
    transaction_time_ind = TimeField()

    class Meta:
        table_name = "expenses"
        primary_key = CompositeKey(
            "current_balance", "transaction_date_ger", "transaction_time_ger"
        )


class TransactionTag(BaseModel):
    merchant_name = CharField(primary_key=True)
    tag = IntegerField()

    class Meta:
        table_name = "transaction_tag"


if __name__ == "__main__":
    pass
