# coding:utf-8


from Service.campusManage import CampusManage
from Service.redis_service import RedisService


class StuService(object):

    @staticmethod
    def get_preview_course():
        campus_li = CampusManage.get_all()
        for campus in campus_li:
            course_li = RedisService.get_selcourse(campus.get("id"))
            campus["course_li"] = course_li

        return campus_li

    @staticmethod
    def get_preview_bycaid(caid):
        return RedisService.get_selcourse(caid)

    @staticmethod
    def count_gpaandcredits(achi_li):
        crd_sum = 0
        achi_sum = 0
        gp_sum = 0
        for achi in achi_li:
            if achi.get("isgreat") == "是":
                crd_sum += achi.get("credit")
                achi_sum += 1
                gp_sum += achi.get("gradepoint")

        return crd_sum, gp_sum/achi_sum


