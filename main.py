import hashlib
import models
import os
import os.path

def init():
    models.db.connect()
    models.db.create_tables([models.Entry])

def digest(file_path):
    h = hashlib.sha1()
    file = open(file_path, 'rb')
    buf = file.read(8192)
    while len(buf) > 0:
        h.update(buf)
        buf = file.read(8192)
    return h.hexdigest()


def traverse(path):
    path = os.path.abspath(path)
    for (dir_path, dirs, files) in os.walk(path):
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)

            entry = models.Entry(path=file_path)
            entry.size = os.path.getsize(file_path)
            entry.last_modified = os.path.getmtime(file_path)
            entry.hash_str = digest(file_path)
            entry.save()
