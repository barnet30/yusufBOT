import psycopg2

class study:

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

    def get_id_course_by_name(self,course_name):
        """Getting id by course name"""
        with self.connection:
            self.cursor.execute('SELECT * FROM "pacanSchema".course WHERE name = %s', (course_name,))
            answer = self.cursor.fetchall()
            try:
                return answer[0][0]
            except:
                return 'Not Found'

    def add_new_student(self,sid, sname, ssurname, idzach, idgroup):
        """Add new student at database"""
        with self.connection:
            sql_query = 'insert into "pacanSchema".student(id, name, surname, idzach, idgrou) values ({student[0]!r}, {student[1]!r}, ' \
                        '{student[2]!r}, {student[3]!r}, {student[4]!r})'.format(
                student=[sid, sname, ssurname, idzach, idgroup])
            self.cursor.execute(sql_query)
            self.connection.commit()

    def check_stud_in_course(self,sid, cid):
        """Checking whether there is a student at this course"""
        with self.connection:
            self.cursor.execute('select * from "pacanSchema".student_course where student_id=%d and course_id=%d' % (sid, cid,))
            answer = self.cursor.fetchall()
            if len(answer) == 0:
                return False
            else:
                return True

    def stud_join_course(self,sid, cid):
        """Add student at course"""
        with self.connection:
            sql_query = 'insert into "pacanSchema".student_course (student_id, course_id) values ({student[0]!r}, {student[1]!r})'.format(
                student=[sid, cid])
            self.cursor.execute(sql_query)
            self.connection.commit()

    def delete_stud_from_course(self,sid, cid):
        """Delete student from course"""
        with self.connection:
            sql_query = 'delete from "pacanSchema".student_course where student_id={} and course_id={}'.format(sid, cid)
            self.cursor.execute(sql_query)
            self.connection.commit()


    def close(self):
        """Closing database"""
        self.connection.close()




    # def add_subscriber(self,user_id, status=True):
    #     """Add new subscriber"""
    #     with self.connection:
    #         self.cursor.execute("""INSERT INTO subscribers (user_id, status)
    #                             VALUES (%s,%s)""",(user_id,status))
    #         self.connection.commit()
    #
    # def get_subscriptions(self, status = True):
    #     """Get active subscribers"""
    #     with self.connection:
    #         try:
    #             self.cursor.execute("SELECT * FROM subscribers WHERE status = (%s)",(status,))
    #             query_results = self.cursor.fetchall()
    #             return query_results
    #         except:
    #             pass
    #
    # def subscriber_exist(self,user_id):
    #     """Checking whether there is a user in the database"""
    #     with self.connection:
    #         try:
    #             self.cursor.execute("SELECT * FROM subscribers WHERE user_id = (%s)",(user_id,))
    #             query_results = self.cursor.fetchall()
    #             return bool(len(query_results))
    #             self.connection.commit()
    #         except:
    #             return False
    #
    # def update_subscription(self, user_id, status):
    #     """Update status subscribe"""
    #     with self.connection:
    #         return self.cursor.execute("UPDATE subscribers SET status = %s WHERE user_id = %s",(status,user_id))