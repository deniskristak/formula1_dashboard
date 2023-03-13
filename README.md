## First setup:
Create a new venv environment:
```bash
python -m venv .venv
```

Activate venv environment (sets you environment so that it uses that specific python interpreter).<br> 
**Do this anytime you run any command in this project**
```bash
source ./venv/bin/activate
```

Install required packages (after setting environment in the previous step):
```bash
pip install -r requirements.txt
```

Create database:
```bash
python manage.py migrate
```

Populate database with **NECESSARY DATA** (drivers, teams, races ... )

*NOTE: If you need to reset database, run `remove_all_from_database` first. Be careful with that one.*
```bash
python manage.py populate_database
```

Populate database with **REAL RESULT** data:
```bash
python manage.py populate_db_real_results
```

Populate database with **REAL BETS** data:
```bash
python manage.py populate_db_real_bets
```

Calculate **SCORES**:
```bash
python manage.py assign_scores
```

## Usage:
Activate the virtual environment:
```bash
source .venv/bin/activate
```

Run the server:
```bash
python manage.py runserver
```
A message should appear: `Starting development server at http://127.0.0.1:8000/`
Go to that localhost address

## Notes
1. DB used - db.sqlite3 for development, postgresql in production
2. If you want to wipe the database
    #### Be careful with this one
    Remove all data about drivers, bets, races etc. from database.
    ```bash
    python manage.py remove_all_from_database
    ```
3. To populate database with test **RESULTS**, run `python manage.py populate_db_test_results`
