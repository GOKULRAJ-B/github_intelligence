FROM apache/superset:4.1.1

USER root

RUN pip install --no-cache-dir psycopg2-binary

COPY init.sh /init.sh
RUN chmod +x /init.sh

USER superset