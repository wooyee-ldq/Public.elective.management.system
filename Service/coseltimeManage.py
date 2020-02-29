# coding:utf-8
import time

from Log.exceptionLog import ExceptionLog
from Model.model import Coseltime, db


class CoseltimeManage(object):

    @staticmethod
    def list_to_dict(li):
        """把选课记录对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        ny = ["否", "是"]

        for seltime in li:
            data = {
                "id": seltime.id,
                "cretime": seltime.cretime,
                "updtime": seltime.updtime,
                "starttime": seltime.starttime,
                "endtime": seltime.endtime,
                "remark": seltime.remark,
                "isend": ny[seltime.isend],
                "campus": seltime.campus,
                "level": seltime.level
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        try:
            seltime_li = Coseltime.query.all()
            return cls.list_to_dict(seltime_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_id(cls, id):
        try:
            seltime = Coseltime.query.get(id)
            if seltime is None:
                return seltime

            else:
                return cls.list_to_dict(seltime)[0]

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @classmethod
    def get_end(cls):
        try:
            seltime = Coseltime.query.filter_by(isend=1)
            return cls.list_to_dict(seltime)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @staticmethod
    def add(starttime, endtime, caid, lid, remark=""):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        seltime = Coseltime(
            cretime=now_time,
            updtime=now_time,
            starttime=starttime,
            endtime=endtime,
            remark=remark,
            isend=0,
            lid=lid,
            caid=caid
        )
        try:
            db.session.add(seltime)
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

    # @staticmethod
    # def update_over(id_li):
    #
    #     if len(id_li) <= 0:
    #         return False
    #
    #     for id in id_li:
    #         try:
    #             seltime = Coseltime.query.get(int(id))
    #             seltime.isend = 1
    #             db.session.add(seltime)
    #
    #         except Exception as e:
    #             print(e)
    #             ExceptionLog.model_error(e.__str__())
    #             try:
    #                 db.session.rollback()
    #             except Exception as ex:
    #                 print(ex)
    #                 ExceptionLog.other_error(ex.__str__())
    #             return False
    #
    #     try:
    #         db.session.commit()
    #         return True
    #
    #     except Exception as e:
    #         print(e)
    #         ExceptionLog.model_error(e.__str__())
    #         try:
    #             db.session.rollback()
    #         except Exception as ex:
    #             print(ex)
    #             ExceptionLog.other_error(ex.__str__())
    #         return False
    #
