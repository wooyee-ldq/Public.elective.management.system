# coding:utf-8
import time

from Log.exceptionLog import ExceptionLog
from Model.myRedis import MyRedis
from Model.model import db, Coseltime, Courses, Selcourses
import json

from Tool.encryption import Encryption


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
    def judge_can_saveachi(caid):
        """判断是否可以录入成绩"""
        try:
            r = MyRedis.get_redis()
            seltime_num = r.hlen("seltime" + str(caid))
            if seltime_num == 0:
                return True
            return False
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
            r.hset("selcourse"+str(course.get("caid")), str(course.get("id")), json.dumps(course))

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            raise e

    @staticmethod
    def get_selcourse(caid):
        """获取缓存中对应校区的课程信息"""
        r = MyRedis.get_redis()
        course_li = r.hvals("selcourse"+str(caid))
        sel_li = list()
        for course in course_li:
            sel_li.append(json.loads(course))
        return sel_li

    @staticmethod
    def get_selnum(caid, cid):
        """获取课程剩余人数"""
        try:
            r = MyRedis.get_redis()
            course = r.hget("selcourse"+str(caid), str(cid))
            if course is None:
                return 0
            course = json.loads(course)
            return int(course.get("cnum"))
        except Exception as e:
            print(e)
            ExceptionLog.other_error(e.__str__())
            return 0

    @staticmethod
    def selnum_sub1(caid, cid):
        """课程人数减少1操作"""
        try:
            r = MyRedis.get_redis()
            course = r.hget("selcourse"+str(caid), str(cid))
            if course is None:
                return False
            course = json.loads(course)
            num = int(course.get("cnum"))
            cnum = num - 1 if num > 0 else None
            if cnum is None:
                # r.hdel("selcourse"+str(caid), str(cid))
                # 原来是要删除选完的课程，但是后面因为要退选，所以这里不再删除
                return False
            course["cnum"] = cnum
            r.hset("selcourse"+str(caid), str(cid), json.dumps(course))
            return True

        except Exception as e:
            print(e)
            ExceptionLog.other_error(e.__str__())
            return False

    @staticmethod
    def selnum_sum1(caid, cid):
        """课程人数加1操作"""
        try:
            r = MyRedis.get_redis()
            course = r.hget("selcourse" + str(caid), str(cid))
            if course is None:
                return False
            course = json.loads(course)
            cnum = int(course.get("cnum")) + 1
            course["cnum"] = cnum
            r.hset("selcourse" + str(caid), str(cid), json.dumps(course))
            return True

        except Exception as e:
            print(e)
            ExceptionLog.other_error(e.__str__())
            raise e

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

    @staticmethod
    def preview_sel(sno, cids):
        """保存预选课程到redis缓存"""
        try:
            r = MyRedis.get_redis()
            name = "preview" + str(sno)
            r.set(name, cids, ex=60 * 60 * 24 * 7)  # 预选的课程一个星期内有效

        except Exception as ex:
            print(ex)
            ExceptionLog.other_error(ex.__str__())
            raise ex

    @staticmethod
    def del_preview(sno):
        """删除预选课程redis缓存"""
        try:
            r = MyRedis.get_redis()
            name = "preview" + str(sno)
            r.delete(name)

        except Exception as ex:
            print(ex)
            ExceptionLog.other_error(ex.__str__())
            raise ex

    @staticmethod
    def save_sel(sno, cids):
        """保存选课信息redis缓存"""
        try:
            r = MyRedis.get_redis()
            name = "sel" + str(sno)
            r.set(name, str(cids), ex=60 * 60 * 4)  # 选课提交成功后4个小时内可以退选

        except Exception as ex:
            print(ex)
            ExceptionLog.other_error(ex.__str__())
            raise ex

    @classmethod
    def judge_and_remove(cls, sid, sno, cid, caid):
        """判断是否可以退选课程，可以则调用退选课程操作函数"""
        tip = "退课失败！"
        try:
            r = MyRedis.get_redis()
            name = "sel" + str(sno)
            cids = r.get(name)
            tip = "超过退课时间，退课失败！"
            if cids is None:
                return False, tip
            cid_li = str(cids).split(",")
            for cid1 in cid_li:
                if str(cid) == cid1:
                    bl = cls.remove_sel(sid, cid, caid)
                    if bl:
                        cid_li.remove(cid1)
                        ln = len(cid_li)
                        cids = ""
                        if ln > 0:
                            for i in range(ln):
                                cid = str(cid_li[i])
                                if i == ln - 1:
                                    cids = cids + cid
                                    continue
                                cids = cids + cid + ","
                            cls.save_sel(sno, cids)
                        elif ln == 0:
                            cls.save_sel(sno, "")
                        tip = "退课成功！"
                        return True, tip
                    else:
                        tip = "退课失败！"
                        break
            return False, tip

        except Exception as ex:
            print(ex)
            ExceptionLog.model_error(ex.__str__())
            return False, tip

    @classmethod
    def remove_sel(cls, sid, cid, caid):
        """退选课程操作"""
        try:
            sel = Selcourses.query.filter_by(sid=int(sid), cid=int(cid)).first()
            db.session.delete(sel)
            cls.selnum_sum1(caid, cid)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @staticmethod
    def get_preview(sno):
        """获取学生预选课程信息"""
        try:
            r = MyRedis.get_redis()
            cids = r.get("preview"+str(sno))
            pre_li = list()
            if cids is None:
                return pre_li
            cid_li = str(cids).split(",")
            for cid in cid_li:
                course = Courses.query.get(int(cid))
                pre_li.append(Courses.list_to_dict(course))
            return pre_li

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            return list()

    @staticmethod
    def tea_agree(tid):
        try:
            r = MyRedis.get_redis()
            r.lrem("teablacklist", 0, tid)
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def tea_refuse(tid):
        try:
            r = MyRedis.get_redis()
            r.lpush("teablacklist", tid)
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def judgetea_iscan_applycourse(tid):
        try:
            r = MyRedis.get_redis()
            tea_li = r.lrange("teablacklist", 0, -1)
            if tea_li is None:
                tea_li = list()
            for tea in tea_li:
                if tea == str(tid):
                    return False
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def judgestu_iscan_selectcourse(sid):
        try:
            r = MyRedis.get_redis()
            stu_li = r.lrange("stublacklist", 0, -1)
            if stu_li is None:
                stu_li = list()
            for stu in stu_li:
                if stu == str(sid):
                    return False
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def stu_agree(sid):
        try:
            r = MyRedis.get_redis()
            r.lrem("stublacklist", 0, sid)
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def stu_refuse(sid):
        try:
            r = MyRedis.get_redis()
            r.lpush("stublacklist", sid)
            return True
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def get_tea_blacklist():
        try:
            r = MyRedis.get_redis()
            tea_li = r.lrange("teablacklist", 0, -1)
            if tea_li is None:
                tea_li = list()
            return tea_li
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return list()

    @staticmethod
    def get_stu_blacklist():
        try:
            r = MyRedis.get_redis()
            stu_li = r.lrange("stublacklist", 0, -1)
            if stu_li is None:
                stu_li = list()
            return stu_li
        except Exception as e:
            ExceptionLog.model_error(e.__str__())
            return list()


     # @staticmethod
     # def add_new_admintip(self, ):










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


if __name__ == '__main__':
    r = MyRedis.get_redis()
    # r.set("test", str(["1", "2"]))
