FROM postgres:14.5

WORKDIR /code


COPY *.sql /docker-entrypoint-initdb.d/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
LABEL author='John'
LABEL description='Web scraper database image'
LABEL version='1.0'
