# This is a sample Python script.
import psycopg2


def connection():
  con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="2776554",
    host="127.0.0.1",
    port="5432"
  )
  return con

def get_id_course_by_name(course_name):
    con = connection()
    cur = con.cursor()
    #cur.execute('select id from "pacanSchema".course where name="{}"'.format(course_name))
    #cur.execute(' select id from "pacanSchema".course where name=%(name)s' % {'name': course_name})
    cur.execute('SELECT * FROM "pacanSchema".course WHERE name = %s', (course_name, ))
    answer = cur.fetchall()
    con.close()
    try:
      return answer[0][0]
    except:
      return 'Not Found'


def add_new_student(sid, sname, ssurname, idzach, idgroup):
    con = connection()
    cur = con.cursor()
    sql_query = 'insert into "pacanSchema".student(id, name, surname, idzach, idgrou) values ({student[0]!r}, {student[1]!r}, ' \
                '{student[2]!r}, {student[3]!r}, {student[4]!r})'.format(student=[sid, sname, ssurname, idzach, idgroup])
    cur.execute(sql_query)
    con.commit()
    con.close()

def check_stud_in_course(sid, cid):
    con = connection()
    cur = con.cursor()
    cur.execute('select * from "pacanSchema".student_course where student_id=%d and course_id=%d'%(sid,cid, ))
    answer = cur.fetchall()
    con.close()
    if len(answer) == 0:
      return False
    else:
      return True

def stud_join_course(sid, cid):
    con = connection()
    cur = con.cursor()
    sql_query = 'insert into "pacanSchema".student_course (student_id, course_id) values ({student[0]!r}, {student[1]!r})'.format(
      student=[sid, cid])
    cur.execute(sql_query)
    con.commit()
    con.close()


def del_stud_from_course(sid, cid):
    con = connection()
    cur = con.cursor()
    sql_query = 'delete from "pacanSchema".student_course where student_id={} and course_id={}'.format(sid, cid)
    cur.execute(sql_query)
    con.commit()
    con.close()


