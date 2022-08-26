import configparser
import psycopg2
from psycopg2._psycopg import connection


def reset_scheme_tables(conn: connection) -> None:
    delete_tables = """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """

    with conn.cursor() as cursor:
        cursor.execute(delete_tables)
        conn.commit()


def create_tables(conn: connection) -> None:
    favorite_person = """
        CREATE TABLE IF NOT EXISTS favorite_person (
        ID SERIAL PRIMARY KEY,
        vk_id INT NOT NULL UNIQUE
        );
    """

    viewed_person = """
        CREATE TABLE IF NOT EXISTS viewed_person (
        ID SERIAL PRIMARY KEY,
        vk_id INT NOT NULL UNIQUE
        );
    """

    interests = """
        CREATE TABLE IF NOT EXISTS interests (
        ID SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
        );
    """

    person = """
        CREATE TABLE IF NOT EXISTS person (
        ID SERIAL PRIMARY KEY,
        vk_id INT NOT NULL UNIQUE,
        name VARCHAR NOT NULL,
        city INT NOT NULL,
        bdate INT NOT NULL,
        sex INT NOT NULL
        );
    """

    user_favorite = """
        CREATE TABLE IF NOT EXISTS user_favorite (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL references person(ID),
        favorite_id INT NOT NULL references favorite_person(ID)
        );
    """

    user_viewed = """
        CREATE TABLE IF NOT EXISTS user_viewed (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL references person(ID),
        viewed_id INT NOT NULL references viewed_person(ID)
        );
    """

    person_int = """
        CREATE TABLE IF NOT EXISTS person_int (
        ID SERIAL PRIMARY KEY,
        personid INT NOT NULL references person(ID),
        intid INT NOT NULL references interests(ID)
        );
    """
    with conn.cursor() as cursor:
        cursor.execute(favorite_person)
        cursor.execute(viewed_person)
        cursor.execute(interests)
        cursor.execute(person)
        cursor.execute(user_favorite)
        cursor.execute(user_viewed)
        cursor.execute(person_int)
        conn.commit()


if __name__ == "__main__":
    path = 'settings.ini'
    config = configparser.ConfigParser()
    config.read(path)

    with psycopg2.connect(database=config.get('SQL', 'database'),
                          user=config.get('SQL', 'user'),
                          password=config.get('SQL', 'password'),
                          port=config.get('SQL', 'port'),
                          host=config.get('SQL', 'host'), ) as conn:

        # clear db after start, in settings.ini 'reset_db': '0' - no, '1' - yes
        try:
            if config.get('SQL', 'reset_db') == '1':
                reset_scheme_tables(conn)
        finally:
            create_tables(conn)
