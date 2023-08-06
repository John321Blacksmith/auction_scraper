FROM postgres:14.5

LABEL author='John'
LABEL description='Web scraper database image'
LABEL version='1.0'

COPY *.sql /docker-entrypoint-initdb.d/