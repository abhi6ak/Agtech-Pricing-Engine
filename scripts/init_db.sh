#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER dwh_user WITH PASSWORD 'dwh_password';
	CREATE DATABASE dwh;
	GRANT ALL PRIVILEGES ON DATABASE dwh TO dwh_user;
	\connect dwh
	GRANT ALL ON SCHEMA public TO dwh_user;
EOSQL
