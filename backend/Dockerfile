FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN python -m pip install --upgrade pip

COPY ./poetry.lock ./pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY ./ /app
