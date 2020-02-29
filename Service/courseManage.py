# coding:utf-8

import time
from Model.model import Courses, db, Teachers
from Log.exceptionLog import ExceptionLog


class CourseManage(object):

    @staticmethod
    def list_to_dict(li):
        """把课程对象列表转换为字典列表"""
        if li is None or len(list(li)) <= 0:  # 如果是空列表返回No
            return list()

        li_dict = list()
        ny = ["否", "是"]
        for course in li:
            data = {
                "id": course.id,
                "cname": course.cname,
                "ctype": course.ctype,
                "classweek": course.classweek,
                "classtime": course.classtime,
                "campus": course.campus,
                "classplace": course.classroom.rname,
                "tid": course.tid,
                "tname": course.teacher.tname,
                "cretime": course.cretime,
                "updtime": course.updtime,
                "credit": course.credit,
                "cnum": course.cnum,
                "ispass": ny[course.ispass],
                "isexamine": ny[course.isexamine],
                "isend": ny[course.isend],
                "caid": course.caid
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        course_li = Courses.query.all()
        return cls.list_to_dict(course_li)

    @classmethod
    def get_apply_course(cls):
        try:
            course_li = Courses.query.filter_by(isexamine=0)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())

    @staticmethod
    def add(cname, ctype, classweek,
            classtime, rid, tid, credit, cnum, caid):

        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        course = Courses(
            cname=cname,
            ctype=ctype,
            classweek=classweek,
            classtime=classtime,
            rid=rid,
            tid=tid,
            cretime=now_time,
            updtime=now_time,
            credit=credit,
            cnum=cnum,
            caid=caid
        )
        try:
            db.session.add(course)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            try:
                db.session.rollback()
            except Exception as ex:
                print(ex)
                ExceptionLog.other_error(ex.__str__())

            return False

    @staticmethod
    def iscan_apply(cweek, ctime, rid):
        """判断该申请的时间地点是否存在"""
        try:
            c = Courses.query.filter_by(classweek=cweek,
                                        classtime=ctime,
                                        rid=rid,
                                        isend=0).first()
            if c is None:
                return False

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
        return True

    @staticmethod
    def delete(cid):
        try:
            course = Courses.query.get(cid)
            db.session.delete(course)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            try:
                db.session.rollback()
            except Exception as ex:
                print(ex)
                ExceptionLog.other_error(ex.__str__())

            return False

    @staticmethod
    def update(cid, cname, ctype, classweek, classtime, classplace, tid, credit):
        try:
            course = Courses.query.get(cid)  # 获取原来的信息

            # 修改信息
            course.cname = cname
            course.ctype = ctype
            course.classweek = classweek
            course.classtime = classtime
            course.classplace = classplace
            course.tid = tid
            course.credit = credit

            db.session.add(course)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            try:
                db.session.rollback()
            except Exception as ex:
                print(ex)
                ExceptionLog.other_error(ex.__str__())

            return False

    @classmethod
    def get_by_id(cls, cid):
        try:
            course = Courses.query.get(cid)
            if course is None:
                return course
            else:
                return cls.list_to_dict([course])[0]

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @classmethod
    def get_by_name(cls, cname):
        try:
            course_li = Courses.query.filter_by(cname=cname)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_type(cls, ctype):
        try:
            course_li = Courses.query.filter_by(ctype=ctype)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_week(cls, classweek):
        try:
            course_li = Courses.query.filter_by(classweek=classweek)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_time(cls, classtime):
        try:
            course_li = Courses.query.filter_by(classtime=classtime)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_place(cls, classplace):
        try:
            course_li = Courses.query.filter_by(classplace=classplace)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_caid(cls, caid):
        try:
            course_li = Courses.query.filter_by(caid=caid)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_tid(cls, tid):
        try:
            course_li = Courses.query.filter_by(tid=tid)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_tid_noend(cls, tid):
        try:
            course_li = Courses.query.filter_by(tid=tid, isend=0)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_tid_noendpass(cls, tid):
        try:
            course_li = Courses.query.filter_by(tid=tid, isend=0, ispass=1, isexamine=1)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_tid_pass(cls, tid):
        try:
            course_li = Courses.query.filter_by(tid=tid, ispass=1, isexamine=1)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_pass(cls, tid):
        """获取教师任教课程业务"""
        try:
            course_li = Courses.query.filter_by(tid=tid, ispass=1, isend=0)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_examine(cls, isexamine):
        try:
            course_li = Courses.query.filter_by(isexamine=isexamine)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_credit(cls, credit):
        try:
            course_li = Courses.query.filter_by(credit=credit)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def course_end(cls, id_li):
        """课程结束操作"""
        for id in id_li:
            try:
                course = Courses.query.get(int(id))
                course.isend = 1
                db.session.add(course)

            except Exception as e:
                print(e)
                ExceptionLog.model_error(e.__str__())
                try:
                    db.session.rollback()
                except Exception as ex:
                    print(ex)
                    ExceptionLog.other_error(ex.__str__())
                return False

        try:
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            try:
                db.session.rollback()
            except Exception as ex:
                print(ex)
                ExceptionLog.other_error(ex.__str__())
            return False

    @classmethod
    def get_load_course(cls):
        """获取要加载缓存的课程"""
        try:
            course_li = Courses.query.filter_by(ispass=1, isexamine=1, isend=0)
            return cls.list_to_dict(course_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

