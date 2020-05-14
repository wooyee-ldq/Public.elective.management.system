# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Campuses


class CampusManage(object):

    @staticmethod
    def list_to_dict(li):
        """把校区对象列表转换为字典列表"""
        if li is None or len(list(li)) <= 0:  # 如果是空列表返回No
            return list()

        li_dict = list()
        for campus in li:
            data = {
                "id": campus.id,
                "caname": campus.caname
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        try:
            campus_li = Campuses.query.all()
            return cls.list_to_dict(campus_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @classmethod
    def get_by_id(cls, caid):
        try:
            campus_li = Campuses.query.get(caid)
            return cls.list_to_dict([campus_li])[0]

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

