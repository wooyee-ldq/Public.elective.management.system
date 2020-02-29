# coding:utf-8


from Model.model import Students, Courses
from Model.model import db
from Tool.encryption import Encryption
from Tool.msghiden import Msghiden


class StuManage(object):
    @staticmethod
    def list_to_dict(li):
        """把学生对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        sex=["女", "男"]

        for stu in li:
            data = {
                "id": stu.id,
                "sno": stu.sno,
                "sname": stu.sname,
                "ssex": sex[stu.ssex],
                "collegename": stu.college.collname,
                "classname": stu.classes.clname,
                "level": stu.level.lname,
                "nativeplace": stu.nativeplace,
                "birthday": stu.birthday,
                "campus": stu.campus.caname,
                "degree": stu.degree,
                "pid": Msghiden.pid_hide(Encryption.base64_decode(stu.pid)),
                "tel": stu.tel,
                "caid": stu.caid,
                "lid": stu.lid
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        stu_li = Students.query.all()
        return cls.list_to_dict(stu_li)

    @classmethod
    def add(cls, sno, sname, ssex, collegename,
            classname, endate, nativeplace, birthday,
            password, tel, campus, degree, pid):

        stu = Students(
            sno=sno,
            sname=sname,
            ssex=ssex,
            collegename=collegename,
            classname=classname,
            endate=endate,
            nativeplace=nativeplace,
            birthday=birthday,
            password=Encryption.md5(password),
            tel=tel,
            campus=campus,
            degree=degree,
            pid=Encryption.base64_encode(pid)
        )

        try:
            db.session.add(stu)
            db.commit()
            return True

        except Encryption as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def delete(cls, sid):
        try:
            stu = Students.query.get(sid)
            db.session.delete(stu)
            db.session.commit()
            return True

        except Encryption as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def update(cls, sid, sno, sname, ssex,
               collegename, classname, endate,
               nativeplace, birthday,tel,
               campus, degree, pid):
        try:
            stu = Students.query.get(sid)  # 获取原来的记录

            # 修改记录信息
            stu.sno = sno
            stu.sname = sname
            stu.ssex = ssex
            stu.collegename = collegename
            stu.classname = classname
            stu.endate = endate
            stu.nativeplace = nativeplace
            stu.birthday = birthday
            stu.tel = tel
            stu.campus = campus
            stu.degree = degree
            if Msghiden.is_hide(pid):
                stu.pid = Encryption.base64_encode(pid)

            # 保存修改记录
            db.session.add(stu)
            db.session.commit()
            return True

        except Encryption as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def get_by_id(cls, sid):
        try:
            stu = Students.query.get(sid)
            if stu is None:
                return stu
            else:
                return cls.list_to_dict([stu])[0]

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_college(cls, collegename):
        try:
            stu_li = Students.query.filter_by(collegename=collegename)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_name(cls, sname):
        try:
            stu_li = Students.query.filter_by(sname=sname)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_class(cls, classname):
        try:
            stu_li = Students.query.filter_by(classname=classname)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_endate(cls, endate):
        try:
            stu_li = Students.query.filter_by(endate=endate)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_campus(cls, caid):
        try:
            stu_li = Students.query.filter_by(caid=caid)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return list()

    @classmethod
    def get_load_stu(cls, caid, lid):
        try:
            stu_li = Students.query.filter_by(caid=caid, lid=lid)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return list()

    @classmethod
    def get_by_degree(cls, degree):
        try:
            stu_li = Students.query.filter_by(degree=degree)
            return cls.list_to_dict(stu_li)

        except Exception as e:
            print(e)
            return list()




