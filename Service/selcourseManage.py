# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Selcourses, db


class SelcourseManage(object):

    @staticmethod
    def list_to_dict(li):
        """把选课记录对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        for cosel in li:
            data = {
                "id": cosel.id,
                "sid": cosel.sid,
                "cid": cosel.cid,
                "cretime": cosel.cretime,
                "stu": cosel.student,
                "course": cosel.course
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        cosel_li = Selcourses.query.all()
        return cls.list_to_dict(cosel_li)

    @classmethod
    def get_by_id(cls, id):
        try:
            cosel = Selcourses.query.get(id)
            if cosel is None:
                return cosel

            else:
                return cls.list_to_dict(cosel)[0]

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @classmethod
    def get_by_sid(cls, sid):
        try:
            cosel_li = Selcourses.query.filter_by(sid=sid)
            return cls.list_to_dict(cosel_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    # @classmethod
    # def get_by_sidnoend(cls, sid):
    #     try:
    #         cosel_li = Selcourses.query.filter_by(sid=sid, isend=0)
    #         return cls.list_to_dict(cosel_li)
    #
    #     except Exception as e:
    #         print(e)
    #         ExceptionLog.model_error(e.__str__())
    #         return None

    @classmethod
    def get_by_cid(cls, cid):
        try:
            cosel_li = Selcourses.query.filter_by(cid=cid)
            return cls.list_to_dict(cosel_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @staticmethod
    def add(sid, cid, isend=0):

        selco = Selcourses(
            sid=sid,
            cid=cid,
            isend=isend
        )
        try:
            db.session.add(selco)
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
    def update(id, isend=1):
        try:
            selco = Selcourses.query.get(id)
            selco.isend = isend
            db.session.add(selco)
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

