import sqlite3

class subscribers:

    def __init__(self,database):
        """Connection to database"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        print("DATABASE CONNECTED")

    def get_subscriptions(self, status = True):
        """Get active subscribers"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exist(self,user_id):
        """Checking whether there is a user in the database"""
        with self.connection:
            result =self.cursor.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?",
                                        (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """Adding a new user"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)",
                                       (user_id,status))

    def update_subscription(self, user_id, status):
        """Update status subscribe"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?",
                                       (status,user_id))

    def close(self):
        """Closing database"""
        self.connection.close()