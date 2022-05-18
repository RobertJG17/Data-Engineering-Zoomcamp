FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2 fastparquet

WORKDIR /app
COPY data-migration-postgres.py data-migration-postgres.py

ENTRYPOINT [ "python", "data-migration-postgres.py" ]