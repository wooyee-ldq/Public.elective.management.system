# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Classrooms


class ClassroomManage(object):

    @staticmethod
    def list_to_dict(li):
        """把教室对象列表转换为字典列表"""
        if li is None or len(list(li)) <= 0:  # 如果是空列表返回No
            return list()

        li_dict = list()
        for room in li:
            data = {
                "id": room.id,
                "rname": room.rname,
                "building": room.building,
                "floor": room.floor,
                "numb": room.numb,
                "caid": room.caid
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_by_id(cls, rid):
        try:
            room = Classrooms.query.get(rid)
            return cls.list_to_dict([room])[0]
        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @staticmethod
    def get_rname(rid):
        try:
            room = Classrooms.query.get(rid)
            if room is not None:
                return str(room.rname)
        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
        return "error"

    @classmethod
    def get_by_caid(cls, caid):
        try:
            room_li = Classrooms.query.filter_by(caid=caid)
            return cls.list_to_dict(room_li)
        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

