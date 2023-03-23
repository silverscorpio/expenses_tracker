from peewee import *

DATABASE = "tracker.db"

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class Tracker(BaseModel):
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
        table_name = "expenses_tracker"
        primary_key = CompositeKey("merchant", "money_spent", "current_balance", "transaction_date_ger")
