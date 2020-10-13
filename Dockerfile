FROM python:3.8

WORKDIR /app/

RUN apt-get update; \
    apt-get install libpq-dev -y;
RUN pip install pipenv

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --deploy --system

COPY . /app/

EXPOSE 80

CMD ["bash"]
