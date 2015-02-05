import peewee

db = peewee.SqliteDatabase('files.sqlite')

class Entry(peewee.Model):
    path = peewee.CharField()
    hash_str = peewee.CharField()
    last_modified = peewee.DateTimeField()
    size = peewee.IntegerField()

    class Meta:
        database = db
