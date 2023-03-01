release: python manage.py migrate

# use (or not use) the following two commands together (and carefully)
# if using separately, you either wipe out everything and don't fill it in or you create duplicates
release: python manage.py remove_all_from_database
release: python manage.py populate_database

web: python manage.py runserver 0.0.0.0:\$PORT