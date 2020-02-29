# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Notices, db
import time


class NoticeManage(object):
    @staticmethod
    def list_to_dict(li):
        """把公告对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        ny = ["否", "是"]

        for notice in li:
            data = {
                "id": notice.id,
                "text": notice.text,
                "cretime": notice.cretime,
                "isover": ny[notice.isover]
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        notice_li = Notices.query.all()
        return cls.list_to_dict(notice_li)

    @classmethod
    def get_by_id(cls, id):
        try:
            notice = Notices.query.get(id)
            if notice is None:
                return notice

            else:
                return cls.list_to_dict(notice)[0]

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_isover(cls, isover):
        try:
            notice_li = Notices.query.filter_by(isover=isover)
            return cls.list_to_dict(notice_li)

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add(text, isover=0):

        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        notice = Notices(
            text=text,
            cretime=now_time,
            isover=isover
        )
        try:
            db.session.add(notice)
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
    def update_over(id_li, isover=1):
        for id in id_li:
            try:
                notice = Notices.query.get(int(id))
                notice.isover = isover
                db.session.add(notice)

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
