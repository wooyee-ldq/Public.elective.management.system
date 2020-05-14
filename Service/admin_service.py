# coding:utf-8


import time

from Log.exceptionLog import ExceptionLog
from Model.model import Courses, db
from Service.coseltimeManage import CoseltimeManage
from Service.courseManage import CourseManage
from Service.redis_service import RedisService


class AdminService(object):

    @staticmethod
    def get_time_stamp(time_str):
        # 先转换为时间数组
        time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳
        time_stamp = int(time.mktime(time_array))
        return time_stamp

    @classmethod
    def get_letter(cls, str1, str2):
        stamp1 = cls.get_time_stamp(str1)
        stamp2 = cls.get_time_stamp(str2)
        if float(stamp1) >= float(stamp2):
            return False
        if float(stamp2) <= float(time.time()):
            return False
        return True

    # @classmethod
    # def set_seltime(cls, stime, etime, remark, caid, lid):
    #     px = float(cls.get_time_stamp(etime)) - float(time.time())
    #     if px <= 0:
    #         return False
    #     bl1 = CoseltimeManage.add(stime, etime, caid, lid, remark)  # 保存记录到mysql
    #     bl2 = RedisService.set_sel_time(stime, etime, caid, lid)  # 添加数据缓存到redis
    #     bl3 = RedisService.load_login_stu(caid, lid, px)  # 添加该校区和年级的学生信息到redis缓存
    #     if bl1 and bl2 and bl3:
    #         return True
    #     return False

    @staticmethod
    def set_seltime(stime, etime, remark, caid, lid):
        """设置选课时段操作"""
        # 查询数据库，并把没有添加到缓存未结束的课程添加到redis
        course_li = CourseManage.get_can_add_to_redis(caid)
        if course_li is not None:
            for course in course_li:
                RedisService.load_agree_course(Courses.list_to_dict(course))

        # 保存记录到mysql，添加数据缓存到redis
        return RedisService.set_sel_time(stime, etime, caid, lid, remark)

    @staticmethod
    def over_seltime(id_li):
        """结束选课时段记录操作"""
        # 把选课时段记录结束,删除选课时段记录的redis缓存
        return RedisService.del_sel_time(id_li)

    @staticmethod
    def course_agree(cid_li):
        """审批同意操作"""
        if cid_li is None:
            return False

        for cid in cid_li:
            try:
                course = Courses.query.get(int(cid))
                course.ispass = 1
                course.isexamine = 1
                db.session.add(course)
                # 把课程添加到缓存
                RedisService.load_agree_course(Courses.list_to_dict(course))
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
            return False

    @staticmethod
    def course_refuse(cid_li):
        """审批拒绝操作"""
        for cid in cid_li:
            try:
                course = Courses.query.get(int(cid))
                course.isexamine = 1
                db.session.add(course)

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
            return False
