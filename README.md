# Pineapple.py

Files management made easy. Pineapple.py is a set of database-backed functions
that helps you through the difficulties in tracking down duplicate files and
move them elsewhere.

## Prerequisites

Pineapple.py is only tested on Python 3.4 and Peewee (database backend) 2.5.
Install the required libraries by typing the following command:

```
pip install -r requirements.txt
```

You might want to use [virtualenv](https://github.com/pypa/virtualenv) to
prevent messing up your environment.

## Usage

Pineapple.py is pretty straightforward. Import functions and use them in an
interactive interpreter or your own script.

A brief example:
```
localhost:~ $ ls
photos		photos2		other
localhost:~ $ python
Python 3.4.0
Type "help", "copyright", "credits" or "license" for more information.
>>> from pineapple import *
>>> init()      # This will set up the database. Call it only once.
>>> for folder in ('photos', 'photos2'):
...     traverse(folder)
Writing chunks until DSC_0256.JPG
Writing chunks until DSC_0512.JPG
>>> check_correctness()
Mismatches: size 0, time 0 of total 322 duplicates.
>>> move_duplicates('other')
Moved 322 duplicate files.
>>> prune()
322 non-existent file entries cleared.
```

## License

See [project license](LICENSE.md).
