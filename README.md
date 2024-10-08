# Url Shortener Django Project

## Objective
The Django project exposes an API endpoint and UI where you can generate a shortened URL for a valid URL. Also, you get back the shortened URL which can be used and redirects you to the original URL. We have used PostgreSQL as our database.

## Setup

1. create a virtual environment
```
python manage.py -m venv venv
```
3. install all the requirements
```
pip install -r requirements.txt
```
4. run migration files
```
python manage.py migrate
```
5. run django servier
```
python manage.py runserver
```

 ## Endpoint usage
 1. To generate shortened URL you the endpoint `{host}/urlmanager/shorten?url=http://instagram.com` with query params `url`
 2. To view the UI use the endpoint `{host}/urlmanager`


 ## PyTest test cases
 All the PyTest cases are put under the folder tests.
 To test all the test cases run
 `pytest`

 To test specific test file
 `pytest <file_path>`
