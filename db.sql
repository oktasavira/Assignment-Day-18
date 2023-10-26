-- Database: postgres

-- DROP DATABASE IF EXISTS postgres;

CREATE DATABASE postgres
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE postgres
    IS 'default administrative connection database';
	
CREATE TABLE results (
  id INT PRIMARY KEY,
  city VARCHAR(255),
  name VARCHAR(255),
  entity VARCHAR(255),
  country CHAR(2),
  sources VARCHAR(255),
  isMobile BOOLEAN,
  isAnalysis BOOLEAN,
  sensorType VARCHAR(255),
  lastUpdated TIMESTAMP,
  firstUpdated TIMESTAMP,
  measurements INT,
  latitude DECIMAL(10, 6),
  longitude DECIMAL(10, 6),
  parameter JSON,
  manufacturer JSON
);