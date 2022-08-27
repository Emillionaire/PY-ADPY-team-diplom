import psycopg2
import configparser

class Sql_table:
    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.conn = psycopg2.connect(database =  self.config.get("SQL", "database"), user = self.config.get("SQL", "user"), password = self.config.get("SQL", "password"))

    def add_person (self, id, name, city, bdate, sex): #добавляет пользователя в таблицу Person
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO Person(vk_id, name, city, bdate, sex)
            VALUES (%s, %s, %s, %s, %s) RETURNING id""", (id, name, city, bdate, sex));
            personid = cur.fetchone()[0]
        self.conn.commit()

    def we_know_him(self, id): #проверяет наличие человека в таблице Person
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT EXISTS(SELECT vk_id FROM person WHERE vk_id = %s) 
            """ % (id));
            a = cur.fetchone()[0]
            return a

