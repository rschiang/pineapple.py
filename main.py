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
        buf = []
        for file_name in sorted(files):
            file_path = os.path.join(dir_path, file_name)
            entry = {
                'path': file_path,
                'size': os.path.getsize(file_path),
                'last_modified': os.path.getmtime(file_path),
                'hash_str': digest(file_path)
            }

            buf.append(entry)
            if len(buf) >= 256:
                print('Writing chunks until', file_name)
                models.Entry.insert_many(buf).execute()
                buf.clear()
