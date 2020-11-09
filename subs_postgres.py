import psycopg2

class subscriptions:

    def __init__(self,database):
        """Connection to database"""
        self.connection = psycopg2.connect(
            database= database,
            user= "postgres",
            host= "127.0.0.1",
            password="godsofsession",
            port= "5432"
        )
        self.cursor = self.connection.cursor()
        print("Database successfully connected!")

    def add_subscriber(self,user_id, status=True):
        """Add new subscriber"""
        with self.connection:
            self.cursor.execute("""INSERT INTO subscribers (user_id, status)
                                VALUES (%s,%s)""",(user_id,status))
            self.connection.commit()

    def get_subscriptions(self, status = True):
        """Get active subscribers"""
        with self.connection:
            try:
                self.cursor.execute("SELECT * FROM subscribers WHERE status = (%s)",(status,))
                query_results = self.cursor.fetchall()
                return query_results
            except:
                pass

    def subscriber_exist(self,user_id):
        """Checking whether there is a user in the database"""
        with self.connection:
            try:
                self.cursor.execute("SELECT * FROM subscribers WHERE user_id = (%s)",(user_id,))
                query_results = self.cursor.fetchall()
                return bool(len(query_results))
                self.connection.commit()
            except:
                return False

    def update_subscription(self, user_id, status):
        """Update status subscribe"""
        with self.connection:
            return self.cursor.execute("UPDATE subscribers SET status = %s WHERE user_id = %s",(status,user_id))


    def close(self):
        """Closing database"""
        self.connection.close()


