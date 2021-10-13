FROM saphyel/python-poetry:1
 
ENV PORT 80
EXPOSE $PORT
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false;poetry install --no-dev -q

COPY . /app

CMD uvicorn --host 0.0.0.0 --port $PORT main:app
