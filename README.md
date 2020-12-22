# PythonFavRepo
Python/Flask based application for displaying popular Python Repos on Github.

## Using the Application
The homepage of the app will display a list of the top 100 Python Repos by default.
You may then use the 'Number of Repos to Request' input field to request more repos.
There is also a checkbox that gives you the option to only use local data (w/o calling the Github API)

## How to run locally

Run the following command:

`docker-compose up --build`

The app should now be available at : http://0.0.0.0:8000

## Running the Tests

The following will run the tests once and exit:

`docker-compose -f docker-compose-test.yaml up --build --abort-on-container-exit`

------------

If you would like to keep the Mysql DB container alive and run the tests multiple times then run the following commands (from the project root directory):

`docker-compose -f docker-compose-test.yaml up --build`

`pipenv install --dev`

`pipenv run pytest`

You may then optionally run the following to view coverage:

`pipenv run coverage run -m pytest`

`pipenv run coverage report`






