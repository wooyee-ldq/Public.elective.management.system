# coding:utf-8
from sqlalchemy import or_

from Model.model import Achievements, db
from Log.exceptionLog import ExceptionLog


class AchievementManage(object):

    @staticmethod
    def list_to_dict(li):
        """把成绩对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        ny = ["否", "是"]

        for achi in li:

            data = {
                "id": achi.id,
                "sid": achi.sid,
                "cid": achi.cid,
                "grade": achi.grade,
                "credit": achi.credit,
                "gradepoint": achi.gradepoint,
                "isgreat": ny[achi.isgreat],
                "course": achi.course,
                "student": achi.student
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        course_li = Achievements.query.all()
        return cls.list_to_dict(course_li)

    @staticmethod
    def add(sid, cid, grade, tid, credit, gradepoint):
        achi = Achievements(sid=sid, cid=cid, grade=grade,
                            tid=tid, credit=credit, gradepoint=gradepoint)
        try:
            db.session.add(achi)
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
    def update(acid, grade):
        """
        备注：该函数功能还没完善，对于分数的改变，还要修改绩点和学分等
        需要了解绩点计算方式
        """
        try:
            achi = Achievements.query.get(acid)
            achi.grade = grade
            db.session.add(achi)
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
    def delete(sid):
        try:
            achi = Achievements.query.get(sid)
            db.session.delete(achi)
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
    def get_by_id(cls, acid):
        try:
            achi = Achievements.query.get(acid)
            if achi is None:
                return achi
            else:
                return cls.list_to_dict(achi)[0]

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @classmethod
    def get_by_sid(cls, sid):
        try:
            achi_li = Achievements.query.filter_by(sid=sid)
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_cid(cls, cid):
        try:
            achi_li = Achievements.query.filter_by(cid=cid, isgreat=-1)
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_cidgreat(cls, cid):
        try:
            achi_li = Achievements.query.filter(Achievements.cid==cid, or_(Achievements.isgreat==0, Achievements.isgreat==1))
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @staticmethod
    def get_by_cid_count(cid):
        count = 0
        try:
            count = Achievements.query.filter_by(cid=cid).count()

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
        return count

    @classmethod
    def get_by_grade(cls, grade):
        try:
            achi_li = Achievements.query.filter_by(grade=grade)
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_credit(cls, credit):
        try:
            achi_li = Achievements.query.filter_by(credit=credit)
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @classmethod
    def get_by_gradepoint(cls, gradepoint):
        try:
            achi_li = Achievements.query.filter_by(gradepoint=gradepoint)
            return cls.list_to_dict(achi_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()
