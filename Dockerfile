FROM python:3.12.3-slim-bookworm

WORKDIR /code

COPY ./Pipfile /code
COPY ./Pipfile.lock /code
COPY ./src /code/src

RUN pip3 install pipenv && pipenv install --deploy --system --ignore-pipfile

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

