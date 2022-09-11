import psycopg2
import configparser
from psycopg2.extras import DictCursor


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

    def take_user_data(self, user_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                SELECT * FROM person WHERE vk_id = %s
            ''', (user_id,))
            self.conn.commit()
            result = cur.fetchone()
            result_dict = {
                'vk_id': result['vk_id'],
                'name': result['name'],
                'city': result['city'],
                'bdate': result['bdate'],
                'sex': result['sex']
            }
            return result_dict

    def add_relevant_persons(self,user_id,  relevant_person_id, name, status=0): # 0 - нейтральное, 1 - избранное, 2 - ЧС
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO user_relevant (person_vk_id, rel_person_id, name, status)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, relevant_person_id, name, status))
            self.conn.commit()

    def take_relevant_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute('''
            SELECT rel_person_id, name FROM user_relevant WHERE person_vk_id = %s and status = 0
            ''', (user_id,))
            self.conn.commit()
            result = cur.fetchall()
        return result

    def make_favorite(self, user_id,  relevant_person_id):
        with self.conn.cursor() as cur:
            cur.execute('''
                UPDATE user_relevant
                SET status = 1
                WHERE person_vk_id = %s and rel_person_id = %s
            ''', (user_id, relevant_person_id))
            self.conn.commit()

    def show_favorites(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute('''
            SELECT rel_person_id, name FROM user_relevant WHERE person_vk_id = %s and status = 1
            ''', (user_id,))
            self.conn.commit()
            result = cur.fetchall()
        return result



# mmm =Sql_table()
# mmm.add_all_persons('5544')
# mmm.add_relevant_persons('95181270', '2971071')