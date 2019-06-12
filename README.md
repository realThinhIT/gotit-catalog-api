# Catalog API System

## Project Description

This is a web services system for the catalog web app, as a part in the SE training program at Got It.

This project is written in Python 2.7 and is being maintained by Thinh Nguyen (Victor), reviewed by Mr. Kien.

## Installation and Setup

1. Install [Python 2.7](https://www.python.org/download/releases/2.7/) on your machine.

2. Clone this project.
```
mkdir ~/gotit-catalog-api
cd ~/gotit-catalog-api
git clone https://github.com/realThinhIT/gotit-catalog-api.git .
```

3. Create an virtual environment with [Virtualenv](https://virtualenv.pypa.io/en/stable/):
```
pip install virtualenv
cd ~/gotit-catalog-api
virtualenv venv
source ~/gotit-catalog-api/venv/bin/activate
```

4. Install project dependencies:
```
cd ~/gotit-catalog-api
pip install -r requirements.txt
```