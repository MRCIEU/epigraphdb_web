FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./poetry.lock ./pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY ./ /app
