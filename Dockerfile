FROM saphyel/python-poetry:1
 
ENV PORT 80
EXPOSE $PORT
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false;poetry install --no-dev -q

COPY . /app

CMD gunicorn main:app --bind=0.0.0.0:$PORT
