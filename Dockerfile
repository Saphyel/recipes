FROM python:3.9-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PORT 80
EXPOSE $PORT
WORKDIR /app

RUN pip install poetry;poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev

COPY . /app

CMD gunicorn main:app --bind=0.0.0.0:$PORT
