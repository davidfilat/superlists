FROM python:latest
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgres://django:07oPXppfgZw7riYUvNMM@db:5432/superlists
ENV EMAIL_PASSWORD 'tczqygjjuffxyawm'
RUN mkdir /code
WORKDIR /code
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN pip install -U pipenv
RUN pipenv install --system --dev --deploy --ignore-pipfile
ADD . /code/
RUN python manage.py collectstatic --no-input

