# coding:utf-8
import time

from Log.exceptionLog import ExceptionLog
from Model.myRedis import MyRedis
from Model.model import db, Coseltime
import json


class RedisService(object):

    @staticmethod
    def set_sel_time(stime, etime, caid, lid, remark=""):
        """设置选课开放时间段，把该设置加入redis缓存，提高选课性能"""
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        seltime1 = Coseltime(
            cretime=now_time,
            updtime=now_time,
            starttime=stime,
            endtime=etime,
            remark=remark,
            isend=0,
            lid=lid,
            caid=caid
        )

        seltime = {
            "caid": caid,
            "lid": lid,
            "stime": stime,
            "etime": etime
        }
        try:
            db.session.add(seltime1)
            r = MyRedis.get_redis()
            r.hset("seltime" + str(caid), str(lid), json.dumps(seltime))
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
    def get_time_stamp(time_str):
        # 先转换为时间数组
        time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳
        time_stamp = int(time.mktime(time_array))
        return time_stamp

    @classmethod
    def is_time_right(cls, str1, str2):
        stamp1 = cls.get_time_stamp(str1)
        stamp2 = cls.get_time_stamp(str2)
        now_time = float(time.time())
        if float(stamp1) >= now_time or float(stamp2) <= now_time:
            return False
        return True

    @classmethod
    def judge_can_sel(cls, stu):
        """判断是否可以选课"""
        r = MyRedis.get_redis()
        num = r.hexists("seltime"+str(stu.caid), str(stu.lid))
        if num <= 0:
            return False
        sel = json.loads(r.hget("seltime" + str(stu.caid), str(stu.lid)))
        stime = sel.get("stime")
        etime = sel.get("etime")
        return cls.is_time_right(stime, etime)

    # @staticmethod
    # def load_login_stu(caid, lid, px):
    #     """加载对应校区和年级的学生信息redis缓存并设置过期时间，提高选课登录性能"""
    #     stu_li = StuManage.get_load_stu(caid, lid)
    #     try:
    #         r = MyRedis.get_redis()
    #         for stu in stu_li:
    #             r.set(str(stu.get("sno")), json.dumps(stu), px=px)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         ExceptionLog.other_error(e.__str__())
    #         return False

    @staticmethod
    def load_agree_course(course):
        """加载审批通过的课程缓存"""
        r = MyRedis.get_redis()
        try:
            r.rpush("selcourse"+str(course.get("caid")), json.dumps(course))

        except Exception as e:
            print(e)
            ExceptionLog.other_error(e.__str__())
            raise e

    @staticmethod
    def get_selcourse(caid):
        """获取缓存中对应校区的课程信息"""
        r = MyRedis.get_redis()
        course_li = r.lrange("selcourse"+str(caid), 0, -1)
        if course_li is None:
            return list()
        sel_li = list()
        for course in course_li:
            sel_li.append(json.loads(course))
        return sel_li

    @staticmethod
    def del_sel_time(id_li):
        """结束选课时段，删除redis缓存的开课设置"""
        r = MyRedis.get_redis()
        for id in id_li:
            try:
                sel = Coseltime.query.get(int(id))

                sel.isend = 1
                db.session.add(sel)

                name = "seltime" + str(sel.caid)
                key = str(sel.lid)
                bl = r.hexists(name, key)
                n = r.hdel(name, key)
                ln = r.hlen(name)
                if ln == 0:
                    r.delete("selcourse" + str(sel.caid))  # 删除对应校区的课程信息缓存
                if n == 0 and bl:
                    return False
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

    @classmethod
    def preview_sel(cls, stu, cid_li):
        """保存预选课程到redis缓存"""
        r = MyRedis.get_redis()
        name = "pre_sel" + str(stu.sno)
        for cid in cid_li:
            sel = {
                "sid": stu.id,
                "cid": int(cid)
            }
            r.rpush(name, sel)  # 存在删除数据问题

    # @staticmethod
    # def load_selcourse():
    #     """加载通过审批的开设课程"""
    #     course_li = CourseManage.get_load_course()
    #     r = MyRedis.get_redis()
    #     for course in course_li:
    #         try:
    #             r.lpush("selcourse", json.dumps(course))
    #
    #         except Exception as e:
    #             print(e)
    #             ExceptionLog.other_error(e.__str__())
    #             return False
    #     return True
    #
    # @staticmethod
    # def get_selcourse():
    #     """获取缓存中的课程信息"""
    #     r = MyRedis.get_redis()
    #     course_li = r.lrange("selcourse", 0, -1)
    #     sel_li = list()
    #     for course in course_li:
    #         sel_li.append(json.loads(course))
    #     return sel_li

