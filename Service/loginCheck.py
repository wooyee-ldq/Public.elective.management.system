# coding:utf-8


from Model.model import Admins, Teachers, Students
from Tool.encryption import Encryption
from Log.exceptionLog import ExceptionLog


class LoginCheck(object):

    @staticmethod
    def admin_pwd_check(user, pwd):
        admin = None

        try:
            user = int(user)
            pwd = Encryption.md5(pwd)
            admin = Admins.query.filter_by(ano=user, password=pwd).first()

        except Exception as e:
            # 保存日志
            ExceptionLog.model_error(e.__str__())
            print(e)

        return admin

    @staticmethod
    def admin_to_dict(admin):
        d = {
            "id": admin.id,
            "ano": admin.ano,
            "issuper": admin.issuper,
            "examine": admin.examine
        }
        return d

    @staticmethod
    def stu_pwd_check(user, pwd):
        stu = None
        try:
            user = int(user)
            pwd = Encryption.md5(pwd)  # 加密转换密码
            # 通过账号和密码查询数据库，获取用户信息对象
            stu = Students.query.filter_by(sno=user, password=pwd).first()

        except Exception as e:
            # 保存日志
            ExceptionLog.model_error(e.__str__())
            print(e)

        return stu  # 返回用户信息对象，如果没有则为None

    @staticmethod
    def stu_to_dict(stu):
        sex = ["女", "男"]
        d = {
            "id": stu.id,
            "sno": stu.sno,
            "sname": stu.sname,
            "ssex": sex[stu.ssex],
            "collegename": stu.college.collname,
            "classname": stu.classes.clname,
            "level": stu.level.lname,
            "nativeplace": stu.nativeplace,
            "birthday": stu.birthday,
            "tel": stu.tel,
            "campus": stu.campus.caname,
            "degree": stu.degree,
            "pid": Encryption.base64_decode(stu.pid)
        }
        return d

    @staticmethod
    def tea_pwd_check(user, pwd):
        tea = None

        try:
            user = int(user)
            pwd = Encryption.md5(pwd)
            tea = Teachers.query.filter_by(tno=user, password=pwd).first()

        except Exception as e:
            # 保存日志
            ExceptionLog.model_error(e.__str__())
            print(e)

        return tea

    @staticmethod
    def tea_to_dict(tea):
        d = {
            "id": tea.id,
            "tno": tea.tno,
            "tname": tea.tname,
            "tsex": tea.tsex,
            "collegename": tea.college.collname,
            "tel": tea.tel
        }
        return d













