FROM python:3.9 as app

EXPOSE 8000

RUN pip install pipenv

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --dev
ADD . /app

RUN export FLASK_APP=pythonfavrepo

ENTRYPOINT ["pipenv", "run"]

CMD ["pytest"]