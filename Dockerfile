FROM saphyel/python:pdm
 
ENV PORT 80
EXPOSE $PORT
WORKDIR /app

COPY pdm.lock pyproject.toml /app/
RUN pdm install --prod

COPY . /app

CMD python -m uvicorn main:app --host 0.0.0.0 --port $PORT
