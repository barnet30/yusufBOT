import psycopg2

class User:
    def __init__(self):
        self.connect = psycopg2.connect(
            database = "UserInfo",
            user = "postgres",
            password = "zifumu06",
            host = "127.0.0.1",
            port = "5432"
        )

# Получаем id всех пользователей
    def get_all_id(self):
        cursor = self.connect.cursor()
        request = "SELECT id FROM user"
        result = cursor.execute(request).fetchall()
        return [i[0] for i in result]

    # Добавляем нового пользователя
    def add_id_to_db(self, user_id):
        cursor = self.connect.cursor()
        request = "INSERT INTO user(id, stat) VALUES(?, ?)"
        cursor.execute(request, (user_id, 0))
        self.connect.commit()