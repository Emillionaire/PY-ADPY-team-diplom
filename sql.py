import psycopg2
import configparser

# CREATE TABLE IF NOT EXISTS Interests (
# Id SERIAL PRIMARY KEY,
# name VARCHAR (850) NOT null
# );
#
# CREATE TABLE IF NOT EXISTS Person (
# Id SERIAL PRIMARY KEY,
# vk_id INTEGER NOT null,
# name VARCHAR (850) NOT null,
# city VARCHAR (850) NOT null,
# bdate INTEGER NOT null
# );
#
# CREATE TABLE IF NOT EXISTS Person_int (
# PersonID INTEGER REFERENCES Person(Id),
# IntID INTEGER REFERENCES Interests(Id),
# CONSTRAINT pkPI PRIMARY KEY (PersonID, IntID)
# );

class Sql_table:
    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.conn = psycopg2.connect(database =  self.config.get("SQL", "database"), user = self.config.get("SQL", "user"), password = self.config.get("SQL", "password"))

    def add_person (self, id, name, city, bdate, sex):
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO Person(vk_id, name, city, bdate, sex)
            VALUES (%s, %s, %s, %s, %s) RETURNING id""", (id, name, city, bdate, sex));
            personid = cur.fetchone()[0]
        self.conn.commit()