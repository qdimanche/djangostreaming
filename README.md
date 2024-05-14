# Streaming Library App

The Streaming Library App is a web application designed to manage a digital movie library. It enables users to seamlessly integrate movie data from the OMDB API, offering functionalities to add new movies, delete existing ones (not currently available), and browse the movie collection. Developed with Python and the Django framework.

## Requirements

To run the Streaming Library App, you will need the following:

- Python 3.8 or higher
- Django 3.2 or higher
- requests library (version 2.26.0 or higher)
- An OMDB API key (register for a free key at http://www.omdbapi.com/ and copy it to a file named `API_KEY` in the root directory of the project)

Ensure that Python and pip are installed on your system. You can then install Django and requests using pip:

```bash
pip install django==3.2
pip install requests==2.26.0
```

## Modifying the Models

When you need to modify your models (located in `streaming_app/models.py`), follow these steps to ensure your database schema is updated accordingly:

1. Make your changes to the model. For example, adding a new field or changing an existing one.
2. Run `python manage.py makemigrations` to create a migration file for these changes.
3. Apply the migration to your database by running `python manage.py migrate`.

## Flushing the Database

If you need to reset your database, removing all data without affecting the schema, you can flush the database. This action will remove all data from your tables but keep the tables themselves:

1. Run `python manage.py flush`.
2. Confirm the action when prompted. This will delete all data from your database.
