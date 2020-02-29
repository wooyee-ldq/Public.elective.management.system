# coding:utf-8


"""后台数据表管理模型类模块"""
from flask_admin.contrib.sqla import ModelView


class AdminsModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "ano": "账号",
        "password": "密码",
        "pwd": "初始密码",
        "issuper": "超级管理员",
        "examine": "审批权限"
    }

    # 设置可搜索字段
    column_searchable_list = ('id', 'ano')

    # 设置过滤器
    column_filters = ('id', 'ano', 'issuper', 'examine')

    # 实现on_model_change方法
    def on_model_change(self, form, model, is_created):
        pwd = form.password.data
        if is_created is True:
            model.set_pwd(pwd)
        else:
            from Model.model import Admins
            adm = Admins.query.get(model.id)
            if adm.password != pwd:
                model.set_pwd(pwd)


class ClassesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "clname": "班级名称",
        "collid": "学院ID",
        "caid": "校区ID",
        "lid": "年级ID",
        "level.lname": "年级",
        "college.collname": "学院",
        "campus.caname": "校区"
    }

    # 设置显示的字段
    column_list = ('id', 'clname', 'level.lname', 'college.collname', 'campus.caname')

    # 设置可搜索字段
    column_searchable_list = ('id', 'clname')

    # 设置过滤器
    column_filters = ('id', 'clname', 'collid', 'caid')


class CampusesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "caname": "校区名称"
    }

    # 设置可搜索字段
    column_searchable_list = ('id', 'caname')

    # 设置过滤器
    column_filters = ('id', 'caname')


class CollegesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "collname": "学院名称",
        "caid": "校区ID",
        "campus.caname": "校区"
    }

    # 设置显示的字段
    column_list = ('id', 'collname', 'campus.caname')

    # 设置可搜索字段
    column_searchable_list = ('id', 'collname')

    # 设置过滤器
    column_filters = ('id', 'collname', 'caid')


class ClassroomsModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "rname": "教室号",
        "building": "教学楼号",
        "floor": "楼层号",
        "numb": "教室层序号",
        "caid": "校区ID",
        "campus.caname": "校区"
    }

    # 设置显示的字段
    column_list = ('id', 'rname', 'building', 'floor', 'numb', 'campus.caname')

    # 设置可搜索字段
    column_searchable_list = ('id', 'rname')

    # 设置过滤器
    column_filters = ('id', 'rname', 'building', 'floor', 'numb', 'caid')


class CoursesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "cname": "课程名称",
        "ctype": "课程类型",
        "classweek": "上课星期",
        "classtime": "上课时间",
        "caid": "校区ID",
        "rid": "教室ID",
        "tid": "教师ID",
        "teacher.tname": "教师",
        "classroom.rname": "教室",
        "campus.caname": "校区",
        "cretime": "创建时间",
        "updtime": "更新时间",
        "cnum": "上课人数",
        "credit": "学分",
        "ispass": "是否通过",
        "isexamine": "是否审批",
        "isend": "是否结束"
    }

    # 设置显示的字段
    column_list = ('id', 'cname', 'ctype',
                   'classweek', 'classtime', 'teacher.tname',
                   'classroom.rname', 'campus.caname', 'cretime', 'updtime', 'cnum',
                   'credit', 'ispass', 'isexamine', 'isend')

    # 设置可搜索字段
    column_searchable_list = ('id', 'cname', 'ctype', 'tid')

    # 设置过滤器
    column_filters = ('id', 'cname', 'ctype', 'classweek', 'classtime', 'rid', 'caid',
                      'tid', 'credit', 'ispass', 'isexamine', 'isend')


class SelcoursesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "sid": "学生ID",
        "cid": "课程ID",
        "student.sname": "学生",
        "course.cname": "课程",
        "cretime": "创建时间"
    }

    column_list = ('id', 'student.sname', 'course.cname', 'cretime')

    # 设置可搜索字段
    column_searchable_list = ('id', 'sid', 'cid')

    # 设置过滤器
    column_filters = ('id', 'sid', 'cid')


class StudentsModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "sno": "账号",
        "sname": "姓名",
        "ssex": "性别",
        "collid": "学院ID",
        "clid": "班级ID",
        "college.collname": "学院",
        "classes.clname": "班级",
        "endate": "入学年份",
        "lid": "年级ID",
        "level.lname": "年级",
        "nativeplace": "生源地/籍贯",
        "birthday": "生日",
        "password": "密码",
        "tel": "电话",
        "caid": "校区ID",
        "campus.caname": "校区",
        "degree": "学位",
        "pid": "身份证"
    }

    column_list = ('id', 'sno', 'sname', 'ssex', 'college.collname', 'classes.clname',
                   'level.lname', 'birthday', 'tel', 'campus.caname', 'degree', 'pid')

    # 设置可搜索字段
    column_searchable_list = ('id', 'sno', 'sname')

    # 设置过滤器
    column_filters = ('id', 'sno', 'sname', 'ssex', 'collid', 'clid',
                      'birthday', 'caid', 'degree', 'level')

    # 实现on_model_change方法
    def on_model_change(self, form, model, is_created):
        pwd = form.password.data
        pid = form.pid.data
        if is_created is True:
            model.set_pwd(pwd)
            model.set_pid(pid)
        else:
            from Model.model import Students
            stu = Students.query.get(model.id)
            if stu.password != pwd:
                model.set_pwd(pwd)
            if stu.pid != pid:
                model.set_pid(pid)


class TeachersModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "tno": "账号",
        "tname": "姓名",
        "tsex": "性别",
        "collid": "学院ID",
        "password": "密码",
        "tel": "电话",
        "caid": "校区ID",
        "college.collname": "学院",
        "campus.caname": "校区"
    }

    column_list = ('id', 'tno', 'tname', 'tsex',
                   'password', 'tel', 'college.collname', 'campus.caname')

    # 设置可搜索字段
    column_searchable_list = ('id', 'tno', 'tname')

    # 设置过滤器
    column_filters = ('id', 'tno', 'tsex', 'collid', 'caid')

    # 实现on_model_change方法
    def on_model_change(self, form, model, is_created):
        pwd = form.password.data
        if is_created is True:
            model.set_pwd(pwd)
        else:
            from Model.model import Teachers
            tea = Teachers.query.get(model.id)
            if tea.password != pwd:
                model.set_pwd(pwd)


class AchievementsModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "sid": "学生ID",
        "cid": "课程ID",
        "grade": "分数",
        "credit": "学分",
        "gradepoint": "绩点",
        "isgreat": "是否有效",
        "student.sname": "学生",
        "course.cname": "课程",
        "course.teacher.tname": "课程教师"
    }

    column_list = ('id', 'student.sname', 'course.cname', 'course.teacher.tname', 'grade',
                   'credit', 'gradepoint', 'isgreat')

    # 设置可搜索字段
    column_searchable_list = ('id', 'sid', 'cid', 'grade')

    # 设置过滤器
    column_filters = ('id', 'sid', 'cid', 'grade', 'credit', 'isgreat', 'gradepoint')


class CoseltimeModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "cretime": "创建时间",
        "updtime": "更新时间",
        "starttime": "开始时间",
        "endtime": "结束时间",
        "level.lname": "年级",
        "lid": "年级ID",
        "caid": "校区ID",
        "remark": "备注",
        "campus.caname": "校区"
    }

    column_list = ('id', 'cretime', 'updtime', 'starttime', 'endtime',
                   'level.lname', 'campus.caname', 'remark')

    # 设置可搜索字段
    column_searchable_list = ('id', 'remark')

    # 设置过滤器
    column_filters = ('id', 'cretime', 'updtime', 'starttime', 'endtime', 'level', 'caid')


class LevelsModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "lname": "年级名称"
    }

    # 设置可搜索字段
    column_searchable_list = ('id', 'lname')

    # 设置过滤器
    column_filters = ('id', 'lname')


class NoticesModelView(ModelView):

    # 设置显示主键
    column_display_pk = True

    # 设置字段标签名
    column_labels = {
        "id": "ID",
        "text": "公告内容",
        "cretime": "创建时间",
        "isover": "是否过期"
    }

    # 设置可搜索字段
    column_searchable_list = ('id', 'text')

    # 设置过滤器
    column_filters = ('id', 'cretime', 'isover')

