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
            self.cursor.execute('SELECT * FROM course WHERE name = %s', (course_name,))
            answer = self.cursor.fetchall()
            try:
                return answer[0][0]
            except:
                return 'Not Found'

    def add_new_student(self,sid, sname, ssurname, idzach, idgroup,age):
        """Add new student at database"""
        with self.connection:
            self.cursor.execute("""insert into student(sid, name, surname, idzach, idgrou,age) 
                values (%s,%s,%s,%s,%s,%s)""",(sid,sname,ssurname,idzach,idgroup,age))
            self.connection.commit()

    def check_stud_in_course(self,sid, cid):
        """Checking whether there is a student at this course"""
        with self.connection:
            self.cursor.execute('select * from student_course where student_id=%d and course_id=%d' % (sid, cid,))
            answer = self.cursor.fetchall()
            if len(answer) == 0:
                return False
            else:
                return True

    def stud_join_course(self,sid, cid):
        """Add student at course"""
        with self.connection:
            self.cursor.execute("""insert into student_course (student_id, course_id)
                values (%s,%s)""",(sid,cid))
            self.connection.commit()

    def del_stud_from_course(self,sid, cid):
        """Delete student from course"""
        with self.connection:
            self.cursor.execute("""delete from student_course where student_id={} and course_id={}""".format(sid, cid))
            self.connection.commit()

    def get_grades(self,sid, cid):
        with self.connection:
            self.cursor.execute('select mark from journal where sid={} and cid={}'.format(sid, cid))
            answer = self.cursor.fetchall()
            new_answer = []
            for a in answer:
                new_answer.append(a[0])
            return new_answer

    def get_attendence(self,sid, cid):
        with self.connection:
            self.cursor.execute('select attendance from journal where sid={} and cid={}'.format(sid, cid))
            answer = self.cursor.fetchall()
            new_answer = []
            for a in answer:
                new_answer.append(a[0])
            return new_answer

    def get_age(self,sid):
        with self.connection:
            self.cursor.execute('select age from student where id={}'.format(sid))
            answer = self.cursor.fetchall()
            try:
                return answer[0][0]
            except:
                return 'Not found'

    def get_list_of_students(self,cid):
        with self.connection:
            self.cursor.execute(
                'select * from student where id in (select student_id from student_course where course_id={})'.format(
                    cid))
            answer = self.cursor.fetchall()
            return answer

    def student_hw(self,sid):
        with self.connection:
            self.cursor.execute('select homework from journal where sid={}'.format(sid))
            answer = self.cursor.fetchall()
            new_answer = []
            for a in answer:
                new_answer.append(a[0])
            return new_answer

    def add_new_teacher(self,tid,tname,tsurname):
        with self.connection:
            self.cursor.execute("""insert into teacher(tid,name,surname) 
            values(%s,%s,%s)""",(tid,tname,tsurname))
            self.connection.commit()

    def check_course_password(self,course_name, course_pass):
        with self.connection:
            self.cursor.execute("""select * from course where name = %s and 
            pass = %s""",(course_name,course_pass))
            ans = self.cursor.fetchall()
            return ans

    def teacher_join_course(self,tid,cid):
        with self.connection:
            self.cursor.execute("""insert into teacher_course(teacher_id, course_id)
            values (%s,%s)""",(tid,cid))
            self.connection.commit()


    def close(self):
        """Closing database"""
        self.connection.close()


