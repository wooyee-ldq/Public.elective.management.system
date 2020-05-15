# coding:utf-8
import time

import math

from Model.model import Selcourses, db
from Service.achievementManage import AchievementManage
from Service.campusManage import CampusManage
from Service.redis_service import RedisService


class StuService(object):

    @staticmethod
    def get_preview_course(caid, ctype, week, page, num=10):
        """获取所有可以的预选课程"""
        campus_li = CampusManage.get_all() if caid == -1 else [CampusManage.get_by_id(caid)]
        course_li = list()
        for campus in campus_li:
            course_li.extend(RedisService.get_selcourse(campus.get("id")))

        if week != "all" or ctype != "all":
            for course in course_li[::-1]:
                if week != "all" and ctype != "all":
                    if week != course.get("week") or ctype != course.get("ctype"):
                        course_li.remove(course)
                        continue

                if week != "all" and ctype == "all" and week != course.get("week"):
                    course_li.remove(course)
                    continue

                if week == "all" and ctype != "all" and ctype != course.get("ctype"):
                    course_li.remove(course)
                    continue

        page = page if page > 0 else 1
        sum = len(course_li)  # 总数
        pagenum = math.ceil(sum / num)  # 最大页数
        st = (page - 1) * num if (page - 1) * num < (sum - 1) else (pagenum - 1) * num  # 截取的开始位置
        end = st + num if (st + num) < sum else sum  # 截取的结束位置

        return course_li[st:end], sum, pagenum ,page if page <= pagenum else pagenum

    @staticmethod
    def get_preview_bycaid(caid):
        """获取对应校区可以预选的课程列表"""
        return RedisService.get_selcourse(caid)

    @staticmethod
    def count_gpaandcredits(achi_li):
        """计算平均绩点和已修学分"""
        crd_sum = 0
        achi_sum = 0
        gp_sum = 0
        for achi in achi_li:
            if achi.get("isgreat") == "是":
                crd_sum += achi.get("credit")
                achi_sum += 1
                gp_sum += achi.get("gradepoint")

        return crd_sum, gp_sum/achi_sum if achi_sum > 0 else 0


    @staticmethod
    def count_credit(sid):
        """计算平均绩点和已修学分"""
        achi_li = AchievementManage.get_by_sid(sid)
        crd_sum = 0
        for achi in achi_li:
            if achi.get("isgreat") == "是":
                crd_sum += achi.get("credit")

        return crd_sum


    @staticmethod
    def get_predone(sno):
        """获取预选成功的课程列表"""
        return RedisService.get_preview(sno)

    @staticmethod
    def save_preview(sno, cid_li):
        """保存学生的预选课程"""
        ln = len(cid_li)
        if ln > 3:
            return False
        cids = ""
        for i in range(ln):
            cid = str(cid_li[i])
            if i == ln-1:
                cids = cids + cid
                continue
            cids = cids + cid + ","

        try:
            RedisService.preview_sel(sno, cids)
            return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def save_sel_course(sid, sno, caid, cid_li):
        """保存学生选课信息"""
        ln = len(cid_li)
        if ln > 3:
            return False, ""
        cids = ""
        for i in range(ln):
            try:
                cid = str(cid_li[i])
                num = RedisService.get_selnum(caid, cid)
                if num == 0:
                    continue
                if not RedisService.selnum_sub1(caid, cid):
                    continue
                sel = Selcourses(sid=sid,
                                 cid=cid,
                                 cretime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                db.session.add(sel)
                if i == ln-1:
                    cids = cids + cid
                else:
                    cids = cids + cid + ","

            except Exception as e:
                print(e)
                return False, ""

        try:
            RedisService.save_sel(sno, cids)
            RedisService.del_preview(sno)
            db.session.commit()
            return True, cids
        except Exception as e:
            print(e)
            return False, ""

    @staticmethod
    def remove_sel_course(sid, sno, cid, caid):
        """课程退选操作业务"""
        return RedisService.judge_and_remove(sid, sno, cid, caid)

