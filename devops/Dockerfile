FROM python:3.9 as app

EXPOSE 8000

RUN pip install pipenv

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install
ADD . /app

RUN export FLASK_APP=pythonfavrepo

ENTRYPOINT ["pipenv", "run"]

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8000"]