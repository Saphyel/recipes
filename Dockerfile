FROM python:3.9

WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install poetry;poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev

COPY ./ /app
