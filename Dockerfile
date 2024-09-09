FROM python:3.12.3-slim-bookworm

WORKDIR /code

COPY ./Pipfile /code
COPY ./Pipfile.lock /code
COPY ./src /code/src

RUN pip3 install pipenv && pipenv install --deploy --system --ignore-pipfile

EXPOSE 8585
CMD ["hypercorn", "src.main:app", "--reload", "--bind", "127.0.0.1:8585"]