# PythonFavRepo
Python/Flask based application for displaying popular Python Repos on Github

## How to run locally

Run the following command:

`docker-compose up --build`

The app should now be available at : http://0.0.0.0:8000

## Running the Tests

The following will run the tests once and exit:
`docker-compose -f docker-compose-test.yaml up --build --abort-on-container-exit`

If you would like to keep the Mysql DB alive and run the tests multiple times then run the following commands:

`docker-compose -f docker-compose-test.yaml up --build`

`pipenv install --dev`

`pipenv run pytest`

Optionally to view coverage run:

`pipenv run coverage run -m pytest`

`pipenv run coverage report`


