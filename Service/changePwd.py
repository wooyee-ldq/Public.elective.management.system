# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Model.model import Admins, Students, Teachers, db
from Tool.encryption import Encryption


class ChangePwd(object):

    @staticmethod
    def admin_change_pwd(id, old_pwd, new_pwd1, new_pwd2):

        if new_pwd1 != new_pwd2:
            return False

        old_pwd = Encryption.md5(old_pwd)

        try:
            admin = Admins.query.get(id)
            if admin.password != old_pwd:
                return False

            admin.password = Encryption.md5(new_pwd1)
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

    @staticmethod
    def stu_change_pwd(id, old_pwd, new_pwd1, new_pwd2):

        if new_pwd1 != new_pwd2:
            return False

        old_pwd = Encryption.md5(old_pwd)

        try:
            stu = Students.query.get(id)
            if stu.password != old_pwd:
                return False

            stu.password = Encryption.md5(new_pwd1)
            db.session.add(stu)
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
    def tea_change_pwd(id, old_pwd, new_pwd1, new_pwd2):

        if new_pwd1 != new_pwd2:
            return False

        old_pwd = Encryption.md5(old_pwd)

        try:
            tea = Teachers.query.get(id)
            if tea.password != old_pwd:
                return False

            tea.password = Encryption.md5(new_pwd1)
            db.session.add(tea)
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


