# Catalog API System

## Project Description

This is a web services system for the catalog web app, as a part in the SE training program at Got It.

This project is written in Python 2.7 and is being maintained by Thinh Nguyen (Victor), reviewed by Mr. Kien.

*Documentation:* [https://realthinhit.github.io/gotit-catalog-api-docs/](https://realthinhit.github.io/gotit-catalog-api-docs/)

## Installation and Setup

1. Install [Python 2.7](https://www.python.org/download/releases/2.7/) on your machine.

2. Clone this project.
```
$ mkdir ~/gotit-catalog-api
$ cd ~/gotit-catalog-api
$ git clone https://github.com/realThinhIT/gotit-catalog-api.git .
```

3. Create an virtual environment with [Virtualenv](https://virtualenv.pypa.io/en/stable/):
```
$ pip install virtualenv
$ cd ~/gotit-catalog-api
$ virtualenv venv --python=python2.7
$ source ~/gotit-catalog-api/venv/bin/activate
```

In case virtualenv can't be found in your PATH, try this command instead:

```
$ python -m virtualenv venv --python=python2.7
```

4. Install project dependencies:
```
$ cd ~/gotit-catalog-api
$ pip install -r requirements.txt
```

## Database Setup and Configurations

1. Install [mysql 5.7](https://dev.mysql.com/downloads/mysql/5.7.html) and run the server:

```
$ mysql.server start
```

2. Create a local development database or create other databases corresponding to the environments `dev`, `test`, `production`:

```
$ mysql -u root
mysql> create database catalog_dev
```

3. Config `SQLALCHEMY_DATABASE_URI` URI connector in `main/config` to match your environment setup:

```
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@127.0.0.1:3306/{database_name}'
```

4. Config your secret key, `SECRET_KEY` in `main/config/base.py`.

5. If you want some mockup data for staging, import mockup data using this command **after running the server for the first time.**

```
$ mysql -u {username} -p {database_name} < ./sql/test.sql
```

## Start Server

Use the following commands to configure your preferred development environment or production environment (if needed).

By default, the server will be started in `development` environment.

```
$ export ENVIRONMENT={development/ production} # Default: development
$ export HOST="0.0.0.0" # Default: 0.0.0.0
$ export PORT=5000 # Default: 5000
```

Start the server:

```
$ python app.py
```


## Testing

Use the following command to run tests. All tests are located in `tests/`.

After running this command, you'll get tests results (passed, failed, warning) and code coverage of the `main` folder.

```
$ ./run_tests.sh
```

### Test Data

Test data is located at `./sql/test.sql`.