FROM postgres:latest

ENV POSTGRES_PASSWORD=Kj&hL8+#Sj*f@g1mz
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=website_database

COPY ./website_database.sql /docker-entrypoint-initdb.d/website_database.sql
RUN echo "psql -U postgres -c \"CREATE USER aendraes WITH PASSWORD 'lofqvist1' NOSUPERUSER NOCREATEDB NOCREATEROLE; GRANT ALL PRIVILEGES ON DATABASE website_database TO aendraes;\"" >> /docker-entrypoint-initdb.d/init-user-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh
