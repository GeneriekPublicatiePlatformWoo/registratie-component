CREATE USER odrc;
CREATE DATABASE odrc;
GRANT ALL PRIVILEGES ON DATABASE odrc TO odrc;
-- On Postgres 15+, connect to the database and grant schema permissions.
-- GRANT USAGE, CREATE ON SCHEMA public TO openforms;