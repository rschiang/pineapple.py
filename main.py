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
            if file_name.startswith('.'):
                continue

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

def get_duplicates():
    from models import Entry
    from peewee import fn, SQL
    return (Entry
        .select(Entry.hash_str, fn.COUNT(Entry.hash_str).alias('occurrence'))
        .group_by(Entry.hash_str)
        .having(SQL('occurrence') > 1))

def check_correctness():
    from models import Entry
    size_miss, time_miss, count = 0, 0, 0
    for hash_entry in get_duplicates():
        entries = Entry.select().where(Entry.hash_str == hash_entry.hash_str)
        size, last_modified, path = None, None, None
        for entry in entries:
            if size:
                if entry.size != size:
                    print('Size mismatch:', hash_entry.hash_str, entry.size, size, entry.path)
                    size_miss += 1
                elif entry.last_modified != last_modified:
                    if abs(entry.last_modified - last_modified) < 5:
                        continue
                    print('Time mismatch:', hash_entry.hash_str, entry.last_modified, last_modified, path, entry.path)
                    time_miss += 1
            else:
                size, last_modified, path = entry.size, entry.last_modified, entry.path
        count += 1
    print('Mismatches: size {}, time {} of total {} duplicates'.format(size_miss, time_miss, count))

def query_file(path):
    from datetime import datetime
    print('Size', os.path.getsize(path))
    print('Ctime', datetime.fromtimestamp(os.path.getctime(path)))
    print('Mtime', datetime.fromtimestamp(os.path.getmtime(path)))
    print('Atime', datetime.fromtimestamp(os.path.getatime(path)))
