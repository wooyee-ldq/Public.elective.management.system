# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Levels


class LevelManage(object):

    @staticmethod
    def list_to_dict(li):
        """把校区对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        for level in li:
            data = {
                "id": level.id,
                "lname": level.lname
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        try:
            level_li = Levels.query.all()
            return cls.list_to_dict(level_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()