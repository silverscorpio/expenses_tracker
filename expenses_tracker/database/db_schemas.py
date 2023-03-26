from peewee import *

from expenses_tracker.modules.settings import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Expenses(BaseModel):
    merchant = CharField()
    money_spent = FloatField()
    current_balance = FloatField()
    transaction_date_ger = DateField()
    transaction_time_ger = TimeField()
    old_balance = FloatField()
    tag = CharField()
    transaction_date_ind = DateField()
    transaction_time_ind = TimeField()

    class Meta:
        table_name = "expenses"
        primary_key = CompositeKey("transaction_date_ger", "transaction_time_ger")


class TransactionTag(BaseModel):
    merchant_name = CharField(primary_key=True)
    tag = IntegerField()

    class Meta:
        table_name = "transaction_tag"


if __name__ == "__main__":
    print(DATABASE_PATH)
    # db.connect()
    # db.create_tables([Expenses, TransactionTag])
    # db.close()
