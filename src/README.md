# Fullstack Challenge for Unbabel

This step-by-step is intended to lead you to install this project at your environment.

## Stack

- Python
    - Flask Framework
- PostgreSQL
- Bootstrap 4

## Install

Install using `pip install` all the plugins inside `requirements.txt`

```bash
$ pip install -r requirements.txt
```

For Sass, it's recommended to use Ruby's `gem` command

```bash
$ gem install sass
```

Last but not least, make sure you have `postgresql` installed

## Database

Execute the command below to create the database

### Creating migration files

```bash
$ py app.py db init
```

```bash
$ py app.py db migrate
```

### Recreating database

```bash
$ py app.py recreate_db
```

## Running

To run the app:

```bash
$ py app.py runserver
```

It will run on http://127.0.0.1:5000/
