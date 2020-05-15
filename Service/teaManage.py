# coding:utf-8


from Model.model import Teachers
from Model.model import db
from Tool.encryption import Encryption


class TeaManage(object):

    @staticmethod
    def list_to_dict(li):
        """把教师对象列表转换为字典列表"""
        if len(list(li)) <= 0 or li is None:  # 如果是空列表返回None
            return list()

        li_dict = list()
        sex = ["女", "男"]

        for tea in li:
            data = {
                "id": tea.id,
                "tno": tea.tno,
                "tname": tea.tname,
                "tsex": sex[tea.tsex],
                "collegename": tea.college.collname,
                "tel": tea.tel,
                "campusname": tea.campus.caname,
                "collid": tea.collid,
                "caid": tea.caid
            }

            li_dict.append(data)

        return li_dict

    @classmethod
    def get_all(cls):
        tea_li = Teachers.query.all()
        return cls.list_to_dict(tea_li)

    @classmethod
    def add(cls, tno, tname, tsex, collegename, password, tel):

        tea = Teachers(
            tno=tno,
            tname=tname,
            tsex=tsex,
            collegename=collegename,
            password=Encryption.md5(password),
            tel=tel
        )

        try:
            db.session.add(tea)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def delete(cls, tid):
        try:
            tea = Teachers.query.get(tid)
            db.session.delete(tea)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def update(cls, tid, tno, tname, tsex, collegename, tel):
        try:
            tea = Teachers.query.get(tid)  # 获取原来的记录

            # 修改记录
            tea.tno = tno
            tea.tname = tname
            tea.tsex = tsex
            tea.collegename = collegename
            tea.tel = tel

            # 保存修改记录（更新）
            db.session.add(tea)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def get_by_id(cls, tid):
        try:
            tea = Teachers.query.get(tid)
            if tea is None:
                return tea
            else:
                return cls.list_to_dict([tea])[0]

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_college(cls, collegename):
        try:
            tea_li = Teachers.query.filter_by(collegename=collegename)
            return cls.list_to_dict(tea_li)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_by_name(cls, tname):
        try:
            tea_li = Teachers.query.filter_by(tname=tname)
            return cls.list_to_dict(tea_li)

        except Exception as e:
            print(e)
            return None

