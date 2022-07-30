import psycopg2

class My_db:
    def __init__(self):
        self.conn = psycopg2.connect(database = input('Введите имя базы: '), user = input('Введите имя пользователя: '), password = input('Введите пароль: '))

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS Person(
            Id SERIAL PRIMARY KEY,
            name VARCHAR(300)NOT NULL,
            surname VARCHAR(300)NOT NULL
        );
        """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS F_numbers(
                Id SERIAL PRIMARY KEY,
                PersonID INTEGER NOT NULL REFERENCES Person(Id),
                phone INTEGER,
                CONSTRAINT u_person UNIQUE (personid,phone)
    
            );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Emails(
                Id SERIAL PRIMARY KEY,
                PersonID INTEGER NOT NULL REFERENCES Person(Id),
                email VARCHAR(300) CHECK (email LIKE '%@%'),
                CONSTRAINT u_person UNIQUE (personid,email)
    
            );
            """)
            self.conn.commit()
            print('Успешно')

    def add_client(self, first_name, last_name, email, phones=None):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                INSERT INTO Person(name, surname)
                VALUES (%s, %s) RETURNING id""", (first_name, last_name));
                personid = cur.fetchone()[0]

                cur.execute("""
                INSERT INTO emails(personid, email)
                VALUES (%s, %s)""", (personid, email));
            except psycopg2.errors.CheckViolation:
                print('Неверный e-mail')

        self.conn.commit()

    def add_phone(self, client_id, phone):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                INSERT INTO f_numbers (personid, phone)
                VALUES (%s, %s)""", (client_id, phone)

            );

            except psycopg2.errors.UniqueViolation:
                print('Эти данные уже внесены')
        self.conn.commit()
        print('Телефон добавлен.')

    def change_client(self, client_id, first_name=None, last_name=None, email=None, phones=None):
        with self.conn.cursor() as cur:
            if first_name:
                cur.execute("""
                UPDATE person SET name=%s WHERE id=%s""", (first_name, client_id));
            if last_name:
                cur.execute("""
                UPDATE person SET surname=%s WHERE id=%s""", (last_name, client_id));
            if email:
                cur.execute("""
                UPDATE emails SET email=%s WHERE personid=%s""", (email, client_id));
            if phones:
                cur.execute("""
                UPDATE f_numbers SET phone=%s WHERE personid=%s""", (phones, client_id));
        self.conn.commit()

    def delete_phone(self, client_id, phone):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM f_numbers WHERE id=%s""", (client_id));
        self.conn.commit()

    def delete_client(self, client_id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM emails WHERE id=%s""", (client_id));
            cur.execute("""
            DELETE FROM f_numbers WHERE id=%s""", (client_id));
            cur.execute("""
            DELETE FROM person WHERE id=%s""", (client_id));
        self.conn.commit()

    def find_client(self, first_name=None, last_name=None, email=None, phone=None):
        with self.conn.cursor() as cur:
            if first_name:
                cur.execute("""
                SELECT name, surname, email, phone FROM person p
                left JOIN emails e on p.id = e.personid
                left JOIN f_numbers fn on p.id = fn.personid
                WHERE name=%s""", [first_name]
                            );
            if last_name:
                cur.execute("""
                SELECT name, surname, email, phone FROM person p
                left JOIN emails e on p.id = e.personid
                left JOIN f_numbers fn on p.id = fn.personid
                WHERE surname=%s""", [last_name]
                            );

            if phone:
                cur.execute("""
                SELECT name, surname, email, phone FROM person p
                left JOIN emails e on p.id = e.personid
                left JOIN f_numbers fn on p.id = fn.personid
                WHERE f_number=%s""", [phone]
                            );
            if email:
                cur.execute("""
                SELECT name, surname, email, phone FROM person p
                left JOIN emails e on p.id = e.personid
                left JOIN f_numbers fn on p.id = fn.personid
                WHERE email=%s""", [email]
                            );

            ask = list(cur.fetchall()[0])
            for index, i in enumerate(ask):
                if not i:
                    ask[index] = 'Отсутствует'
            print(f'Имя: {ask[0]}\nФамилия: {ask[1]}\nEmail: {ask[2]}\nТелефон: {ask[3]}')

    def main(self):
        print("""Список команд:
        Создать таблицы: 1
        Добавить клиента: 2
        Добавить телефон: 3
        Изменить данные клиента: 4
        Удалить телефон: 5
        Удалить клиента: 6
        Найти клиента: 7
        Завершить работу: 0
        """)
        while True:
            command = int(input('Что делаем? '))
            if command == 0:
                print('До свидания!')
                break
            if command == 1:
                me.create_db()
            if command == 2:
                name = input('Введите имя: ')
                surname = input('Введите фамилию: ')
                email = input('Введите емайл: ')
                phone = input('Введите телефон или None: ')
                self.add_client(name, surname, email, phone)
            if command == 3:
                client_id = input('Введите id: ')
                phone = input('Введите телефон: ')
                me.add_phone(client_id, phone)
            # if command == 4:
            # if command == 5:
            # if command == 6:
            # if command == 7:



if __name__ == '__main__':
    me = My_db()
    me.main()
    me.conn.close()