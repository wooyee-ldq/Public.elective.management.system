# coding:utf-8


from Model.model import Admins, db
from Log.exceptionLog import ExceptionLog
from Tool.encryption import Encryption
import random


class AdminManage(object):

    @staticmethod
    def list_to_dict(li):
        """把普通管理员对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()

        for admin in li:
            data = {
                "id": admin.id,
                "ano": admin.ano,
                "pwd": admin.pwd,
                "issuper": admin.issuper,
                "examine": admin.examine
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        try:
            admin_li = Admins.query.filter_by(issuper=0)
            return cls.list_to_dict(admin_li)

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return None

    @staticmethod
    def permission_agree(id_li):
        for id in id_li:
            try:
                admin = Admins.query.get(int(id))
                if admin.examine == 0:
                    admin.examine = 1
                    db.session.add(admin)

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

    @staticmethod
    def permission_refuse(id_li):
        for id in id_li:
            try:
                admin = Admins.query.get(int(id))
                if admin.examine == 1:
                    admin.examine = 0
                    db.session.add(admin)

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

    @staticmethod
    def add(ano, password):
        admin = Admins(ano=ano, password=Encryption.md5(password), pwd=password, issuper=0, examine=0)
        try:
            db.session.add(admin)
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
    def fast_add(cls):
        ano = random.randint(1000000000, 4294967295)
        pwd = random.randint(1000000000, 9999999999)
        return cls.add(ano, pwd)



