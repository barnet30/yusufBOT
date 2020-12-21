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

def get_grades(sid,cid):
    con = connection()
    cur = con.cursor()
    cur.execute('select mark from "pacanSchema".journal where sid={} and cid={}'.format(sid,cid))
    answer = cur.fetchall()
    con.close()
    new_answer=[]
    for a in answer:
        new_answer.append(a[0])
    return new_answer

def get_attendence(sid, cid):
    con = connection()
    cur = con.cursor()
    cur.execute('select attendance from "pacanSchema".journal where sid={} and cid={}'.format(sid, cid))
    answer = cur.fetchall()
    con.close()
    new_answer = []
    for a in answer:
        new_answer.append(a[0])
    return new_answer

def get_age(sid):
    con = connection()
    cur = con.cursor()
    cur.execute('select age from "pacanSchema".student where id={}'.format(sid))
    answer = cur.fetchall()
    con.close()
    try:
        return answer[0][0]
    except:
        return 'Not found'

def get_list_of_students(cid):
    con = connection()
    cur = con.cursor()
    cur.execute('select * from "pacanSchema".student where id in (select student_id from "pacanSchema".student_course where course_id={})'.format(cid))
    answer = cur.fetchall()
    con.close()
    return answer

def student_hw(sid):
    con = connection()
    cur = con.cursor()
    cur.execute('select homework from "pacanSchema".journal where sid={}'.format(sid))
    answer = cur.fetchall()
    con.close()
    new_answer = []
    for a in answer:
        new_answer.append(a[0])
    return new_answer

def get_from_journal(cid):
    con = connection()
    cur = con.cursor()
    cur.execute('select * from "pacanSchema".journal where cid = {}'.format(cid))
    answer = cur.fetchall()
    con.close()
    return answer

def assign_grades(sid, cid, grade):
    con = connection()
    cur = con.cursor()
    cur.execute('update "pacanSchema".journal set mark = {} where sid={} and cid={};'.format(grade, sid, cid))
    con.commit()
    con.close()

def get_cid_by_tid(tid):
    con = connection()
    cur = con.cursor()
    cur.execute('select course_id from "pacanSchema".teacher_course where teacher_id = {}'.format(tid))
    answer = cur.fetchall()
    con.close()
    return answer

def assign_attendence(list_of_students, cid, attendence):
    con = connection()
    cur = con.cursor()
    for i in range(len(attendence)):
        cur.execute('update "pacanSchema".journal set attendance = {att[0]!r} where sid = {att[1]!r} and cid={att[2]!r}'.format(att = [attendence[0], list_of_students[i], cid]))
        con.commit()
    con.close()

assign_attendence([1,2,3,4,5], 1, ['н', 'н', 'н', 'н', 'н'])