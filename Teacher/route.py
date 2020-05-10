# coding:utf-8


from flask import render_template, request, jsonify, session, redirect, url_for

from Service.changePwd import ChangePwd
from Service.classroomManage import ClassroomManage
from Service.loginCheck import LoginCheck
from Service.achievementManage import AchievementManage
from Service.noticeManage import NoticeManage
from Service.selcourseManage import SelcourseManage
from Service.stuManage import StuManage
from Service.courseManage import CourseManage
from Service.tea_service import TeaService
from WTF_Form.login_form import LoginForm
from . import app_tea
from Log.loginLog import LoginLog


@app_tea.before_request
def before_request():
    url = request.path
    if len(url.split("/")) > 3:
        tea = session.get("tea")
        if tea is None:
            return render_template("page404.html"), 404


@app_tea.route("/")
def tea_login():
    """返回教师登录页面"""
    form = LoginForm()
    return render_template("teacher/tea_login.html", form=form)


@app_tea.route("/index", methods=["POST"])
def tea_index():
    """登录成功返回教师主页"""
    data = request.form
    user = data.get("username")
    password = data.get("password")
    ip = request.remote_addr

    if user is None or password is None:
        return render_template("page404.html"), 404  # 防止使用postman等工具进行访问

    tea = LoginCheck.tea_pwd_check(user, password)

    if tea is None:
        # 保存日志
        LoginLog.login_error(LoginLog.tea_log_error(user, ip))
        return render_template("teacher/tea_login.html",
                               form=LoginForm(),
                               error="账号或密码错误！")  # 系统提示
    else:
        # 保存日志
        LoginLog.login_success(LoginLog.tea_log_success(user, ip))

        data = LoginCheck.tea_to_dict(tea)
        session["tea"] = tea
        pic = tea.tname[-2:]
        notice_li = NoticeManage.get_by_isover(0)
        if notice_li is None:
            notice_li = list()

        notice_li.reverse()  # 倒序，把最新公告放在前面
        return render_template("teacher/tea_index.html", **data,
                               pic=pic, notice_li=notice_li)


@app_tea.route("/teaExit")
def tea_exit():
    """退出登录操作"""
    session.pop("tea", None)
    return redirect(url_for("app_tea.tea_login"))


@app_tea.route("/changePwd", methods=["POST"])
def change_pwd():
    """教师修改密码操作"""
    tea = session.get("tea")
    if tea is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    data = request.form
    old_pwd = data.get("old_pwd")
    new_pwd1 = data.get("new_pwd1")
    new_pwd2 = data.get("new_pwd2")

    bl = ChangePwd.tea_change_pwd(tea.id, old_pwd, new_pwd1, new_pwd2)
    if bl is True:
        return jsonify({"tip": "修改成功！"})
    else:
        return jsonify({"tip": "修改失败！"})


@app_tea.route("/achievementSavePage")
def achievement_save_page():
    """成绩录入页面"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404
    if TeaService.is_can_saveachi(tea.caid) is False:
        return "选课结束后才能进行成绩录入！"

    course_li = TeaService.get_notachi_li(tea.id)
    return render_template("teacher/achievement_save.html", course_li=course_li)


@app_tea.route("/achievementSave", methods=["POST"])
def achievement_save():
    """成绩录入保存操作"""
    tea = session.get("tea")
    if tea is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    achi_li = request.form.get("achi_li").split(",")

    bl = TeaService.save_achi(achi_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "成绩保存成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "成绩保存失败！"
        })


@app_tea.route("/achievementGet")
def achievement_get():
    """学生成绩查看"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    course_li = TeaService.get_all_achi(tea.id)
    return render_template("teacher/achievement_get.html", course_li=course_li)


@app_tea.route("/achievementChangePage")
def achievement_change_page():
    """返回成绩修改页面"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    course_li = TeaService.get_achi_li(tea.id)
    return render_template("teacher/achievement_change.html", course_li=course_li)


@app_tea.route("/achievementChange", methods=["POST"])
def achievement_change():
    """学生成绩修改"""
    tea = session.get("tea")
    if tea is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    achi_li = request.form.get("achi_li").split(",")

    bl = TeaService.save_achi(achi_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "成绩保存成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "成绩保存失败！"
        })


@app_tea.route("/stuGet")
def stu_get():
    """学生信息查询"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    course_li = TeaService.get_sel_course(tea.id)

    return render_template("teacher/stu_get.html", course_li=course_li)


@app_tea.route("/teaCourseGet")
def tea_course_get():
    """查看任教课程"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    tid = tea.id
    course_li = CourseManage.get_by_pass(tid)

    return render_template("teacher/tea_course_now.html", course_li=course_li)


@app_tea.route("/teaCourseEnd", methods=["POST"])
def tea_course_end():
    """结课操作"""
    tea = session.get("tea")
    if tea is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    id_arr = request.form.get("cid_arr")
    id_li = id_arr.split(",")
    bl = CourseManage.course_end(id_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "结课操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "结课操作失败！"
        })


@app_tea.route("/teaCourseGetall")
def tea_course_getall():
    """教师开课记录"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    tid = tea.id
    course_li = CourseManage.get_by_tid(tid)
    if course_li is None:
        course_li = list()
    return render_template("teacher/tea_course_all.html", course_li=course_li)


@app_tea.route("/courseApplyPage")
def course_apply_page():
    """开课申请页面"""
    tea = session.get("tea")
    if tea is None:
        return render_template("page404.html"), 404

    tid = tea.id
    course_li = CourseManage.get_by_tid_noend(tid)
    room_li = ClassroomManage.get_by_caid(tea.caid)

    return render_template("teacher/course_apply_page.html",
                           course_li=course_li,
                           room_li=room_li)


@app_tea.route("courseApply", methods=["POST"])
def course_apply():
    """提交开课申请"""
    tea = session.get("tea")
    if tea is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })
    data = request.form  # 获取请求体表格形式数据
    cname = data.get("cname")  # 课程名称
    ctype = data.get("ctype")  # 课程类型
    cweek = data.get("cweek")  # 上课星期
    ctime = data.get("ctime") + ":00"  # 上课时间
    rid = data.get("rid")  # 教室号
    credit = data.get("credit")  # 课程学分
    cnum = data.get("cnum")  # 开课人数
    tid = tea.id  # 开课教师id
    caid = tea.caid  # 开课校区id，该校区id是申请教师的校区id，所以本校区开设的课程只能在本校区

    if CourseManage.iscan_apply(cweek, ctime, rid) is True:# 判断开课的时间、地点是否冲突
        return jsonify({
            "bl": 400,
            "tip": cweek + " " + ctime + " 教室:" + ClassroomManage.get_rname(rid) + "已被申请！"
        })

    # 执行课程添加操作，成功返回True
    bl = CourseManage.add(cname, ctype, cweek, ctime, rid, tid, credit, cnum, caid)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "开课申请操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "开课申请操作失败！"
        })


