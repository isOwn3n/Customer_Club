# Customer Club

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/isOwn3n/Customer_Club.git
$ cd Customer_Club
```

ssh:
```sh
$ git clone git@github.com:isOwn3n/Customer_Club.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv .venv
$ source env/bin/activate
```

Then install the dependencies:

```sh
(.venv)$ pip install -r requirements.txt
```
Note the `(.venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `python -m venv`.

Once `pip` has finished downloading the dependencies:
```sh
(.venv)$ cd Customer_Club
(.venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/swagger/`.
