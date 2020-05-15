# coding:utf-8
from Log.exceptionLog import ExceptionLog
from Service.redis_service import RedisService
from .selcourseManage import SelcourseManage
from .courseManage import CourseManage
from .achievementManage import AchievementManage
from Model.model import Achievements, db


class TeaService(object):

    @staticmethod
    def get_sel_course(tid):
        """获取教师开设课程和课程选课记录"""
        course_li = CourseManage.get_by_tid_noend(tid)
        for course in course_li:
            cid = course.get("id")
            sel_li = SelcourseManage.get_by_cid(cid)
            course["stu_li"] = sel_li

        return course_li

    @staticmethod
    def get_notachi_li(tid):
        """获取还没有录入成绩的成绩记录"""
        course_li = CourseManage.get_by_tid_noendpass(tid)
        for course in course_li:
            cid = course.get("id")
            count = AchievementManage.get_by_cid_count(cid)
            if count == 0 or count is None:
                sel_li = SelcourseManage.get_by_cid(cid)
                achi_li = None
                for sel in sel_li:
                    achi_li = list()
                    try:
                        achi = Achievements(sid=sel.get("sid"), cid=sel.get("cid"))
                        db.session.add(achi)
                        achi_li.append(achi)

                    except Exception as e:
                        print(e)
                        ExceptionLog.model_error(e.__str__())
                        try:
                            db.session.rollback()
                        except Exception as e:
                            print(e)
                            ExceptionLog.model_error(e.__str__())
                        course["achi_li"] = list()
                        achi_li = None
                        break

                if achi_li is not None:
                    try:
                        db.session.commit()
                        course["achi_li"] = achi_li

                    except Exception as e:
                        print(e)
                        ExceptionLog.model_error(e.__str__())
                        try:
                            db.session.rollback()
                        except Exception as e:
                            print(e)
                            ExceptionLog.model_error(e.__str__())
                        course["achi_li"] = list()
                else:
                    course["achi_li"] = list()

            else:
                course["achi_li"] = AchievementManage.get_by_cid(cid)

        return course_li

    @staticmethod
    def get_achi_li(tid):
        """通过教师id获取对应课程成绩列表"""
        course_li = CourseManage.get_by_tid_noendpass(tid)
        for course in course_li:
            cid = course.get("id")
            course["achi_li"] = AchievementManage.get_by_cidgreat(cid)
        return course_li

    @staticmethod
    def get_all_achi(tid):
        """获取教师开设所有课程学生成绩"""
        course_li = CourseManage.get_by_tid_pass(tid)
        for course in course_li:
            cid = course.get("id")
            course["achi_li"] = AchievementManage.get_by_cidgreat(cid)
        return course_li

    # @staticmethod
    # def submit_chg_achi(achi_li):
    #     """提交修改成绩的通知"""
    #     newachi_li = list()
    #     for i in range(0, len(achi_li), 3):
    #         try:
    #             acid = int(achi_li[i])
    #             isgreat = int(achi_li[i + 1])
    #             grade = int(achi_li[i + 2])
    #             achi = AchievementManage.get_by_id(acid)
    #             if achi is None:
    #                 return False
    #             achi["newgrade"] = grade
    #             achi["newisgreat"] = isgreat
    #             newachi_li.append(achi)
    #
    #         except Exception as e:
    #             print(e)
    #             ExceptionLog.model_error(e.__str__())
    #             return False
    #

    @staticmethod
    def save_achi(achi_li):
        """保存成绩"""
        for i in range(0, len(achi_li), 3):
            try:
                acid = int(achi_li[i])
                isgreat = int(achi_li[i + 1])
                grade = int(achi_li[i + 2])
            except Exception as e:
                print(e)
                return False
            credit = 0
            gradepoint = 0
            if grade > 100 or grade < 0:
                return False
            try:

                achi = Achievements.query.get(acid)
                if achi.course.isend == 1:
                    return False
                achi.isgreat = isgreat
                achi.grade = grade

                if grade >= 60:
                    credit = achi.course.credit
                    gradepoint = (grade - 50)/10

                achi.credit = credit
                achi.gradepoint = gradepoint
                db.session.add(achi)

            except Exception as e:
                print(e)
                ExceptionLog.model_error(e.__str__())
                try:
                    db.session.rollback()
                except Exception as e:
                    print(e)
                    ExceptionLog.model_error(e.__str__())
                return False

        try:
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            ExceptionLog.model_error(e.__str__())
            try:
                db.session.rollback()
            except Exception as e:
                print(e)
                ExceptionLog.model_error(e.__str__())
            return False

    @staticmethod
    def is_can_saveachi(caid):
        """判断是否可以进行成绩录入"""
        return RedisService.judge_can_saveachi(caid)

