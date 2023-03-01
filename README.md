## First setup:
Install all dependencies into pipenv environment:
```bash
pipenv install
```

If a new dependency is needed, install it with
```bash
pipenv install pandas
```

Activate `pipenv shell` (shell that uses python interpreter with all the required dependencies).
Use this everytime you run any command in this project.
```bash
pipenv shell
```

Create database:
```bash
python manage.py migrate
```

Populate database with test data:
Note - this should only be run once, as it will duplicate the data if ran multiple times on one database.
```bash
python manage.py populate_database
```

## Usage:
Activate pipenv shell
```bash
pipenv shell
```

Run the server:
Activate pipenv shell
```bash
python manage.py runserver
```
A message should appear: `Starting development server at http://127.0.0.1:8000/`
Go to that localhost address

## Notes
1. DB used - db.sqlite3
2. Find the command dedicated to the results processing in `tips_dash/management/commands/edov_cmd.py`
3. Command can be run with `python manage.py edkov_cmd`
4. All additional info (w.r.t retrieval of object from DB, creating new objects etc.) can be found in comments of the command's code
5. Newly created models (results, points) are defined in `tips_dash/models.py`
6. To populate database with test results, run `python manage.py populate_database`

# release: python manage.py remove_all_from_database
# release: python manage.py populate_database