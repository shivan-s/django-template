FROM python:3.8-slim

ENV PYTHONDONTWEITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PIPENV_VERBOSITY -1

WORKDIR /code

# hadolint ignore=DL3013
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install

COPY . /code/

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
