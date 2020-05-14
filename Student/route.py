# coding:utf-8


from flask import render_template, request, jsonify, session, redirect, url_for

from Service.campusManage import CampusManage
from Service.changePwd import ChangePwd
from Service.loginCheck import LoginCheck
from Service.noticeManage import NoticeManage
from Service.redis_service import RedisService
from Service.selcourseManage import SelcourseManage
from Service.achievementManage import AchievementManage
from Service.stu_service import StuService
from WTF_Form.login_form import LoginForm
from . import app_stu
from Log.loginLog import LoginLog


@app_stu.before_request
def before_request():
    url = request.path
    if len(url.split("/")) > 3:
        stu = session.get("stu")
        if stu is None:
            return render_template("page404.html"), 404


@app_stu.route("/")
def stu_login():
    """返回学生登录页面"""
    form = LoginForm()
    return render_template("student/stu_login.html", form=form)


@app_stu.route("/index", methods=["POST"])
def stu_index():
    """登录成功返回学生主页"""
    data = request.form
    user = data.get("username")
    password = data.get("password")
    ip = request.remote_addr

    if user is None or password is None:
        return render_template("page404.html"), 404  # 防止使用postman等工具进行访问

    stu = LoginCheck.stu_pwd_check(user, password)

    if stu is None:
        # 保存日志
        LoginLog.login_error(LoginLog.stu_log_error(user, ip))
        return render_template("student/stu_login.html",
                               form=LoginForm(),
                               error="账号或密码错误！")  # 系统提示
    else:
        # 保存日志
        LoginLog.login_success(LoginLog.stu_log_success(user, ip))

        data = LoginCheck.stu_to_dict(stu)
        # 保存用户session
        session["stu"] = stu
        pic = stu.sname[-2:]
        notice_li = NoticeManage.get_by_isover(0)
        return render_template("student/stu_index.html", **data,
                               pic=pic, notice_li=notice_li)


@app_stu.route("/changePwd", methods=["POST"])
def change_pwd():
    """修改密码操作"""
    stu = session.get("stu")
    if stu is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    # 获取修改密码数据
    data = request.form
    old_pwd = data.get("old_pwd")  # 获取原密码
    new_pwd1 = data.get("new_pwd1")  # 获取新密码
    new_pwd2 = data.get("new_pwd2")  # 获取新确认密码

    bl = ChangePwd.stu_change_pwd(stu.id, old_pwd, new_pwd1, new_pwd2)
    if bl is True:
        return jsonify({"tip": "修改成功！"})
    else:
        return jsonify({"tip": "修改失败！"})


@app_stu.route("/stuExit")
def stu_exit():
    """退出登录操作"""
    session.pop("stu", None)
    return redirect(url_for("app_stu.stu_login"))


@app_stu.route("/courseSelGet")
def course_sel_get():
    """学生选课信息查询"""
    sid = request.form.get("sid")

    cosel_li = SelcourseManage.get_by_sid(sid)
    return jsonify(cosel_li)


@app_stu.route("/gradeGet")
def grade_get():
    """成绩查看页面"""
    stu = session.get("stu")
    if stu is None:
        return render_template("page404.html"), 404

    achi_li = AchievementManage.get_by_sid(stu.id)
    crd_sum, gpa = StuService.count_gpaandcredits(achi_li)
    return render_template("student/grade_get.html",
                           achi_li=achi_li,
                           crd_sum=crd_sum,
                           gpa=gpa)


@app_stu.route("/coursePreview", methods=["POST", "GET"])
def course_preview():
    """课程预览页面"""
    stu = session.get("stu")
    if stu is None:
        return render_template("page404.html"), 404

    data = request.form
    page = int(data.get("page", request.args.get("page", 1)))
    caid = int(data.get("caid", session.get("caid", -1)))
    ctype = data.get("ctype", session.get("ctype", "all"))
    week = data.get("week", session.get("week", "all"))
    session["caid"] = caid
    session["ctype"] = ctype
    session["week"] = week

    course_li, sum, pagenum, page = StuService.get_preview_course(caid, ctype, week, page, 3)
    campus_li = CampusManage.get_all()

    return render_template("student/course_preview.html",
                           campus_li=campus_li,
                           course_li=course_li,
                           page=page,
                           pagenum=pagenum,
                           sum=sum)


@app_stu.route("/previewPage", methods=["POST", "GET"])
def preview_page():
    """课程预选页面"""
    stu = session.get("stu")
    if stu is None:
        return render_template("page404.html"), 404

    crd_sum = StuService.count_credit(stu.id)
    if crd_sum >= 33:
        return render_template("not_allow.html", message="所修学分已满，不需要选课...")

    if RedisService.judge_can_sel(stu):
        return redirect(url_for("app_stu.sel_course_page"))

    data = request.form
    page = int(data.get("page", request.args.get("page", 1)))
    caid = stu.caid
    ctype = data.get("ctype", session.get("ctype", "all"))
    week = data.get("week", session.get("week", "all"))
    session["caid"] = caid
    session["ctype"] = ctype
    session["week"] = week

    course_li, sum, pagenum, page = StuService.get_preview_course(caid, ctype, week, page, 4)
    preview_li = StuService.get_predone(stu.sno)

    return render_template("student/preview_page.html",
                           course_li=course_li,
                           page=page,
                           pagenum=pagenum,
                           sum=sum,
                           preview_li=preview_li)


@app_stu.route("/preview", methods=["POST"])
def preview():
    """预选操作"""
    stu = session.get("stu")
    if stu is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })
    cid_li = request.form.get("cid_li").split(",")
    bl = StuService.save_preview(stu.sno, cid_li)
    if bl:
        return jsonify({"tip": "预选课程成功，预选的课程一个星期内有效！"})
    else:
        return jsonify({"tip": "预选课程失败！"})


@app_stu.route("/courseRecord")
def course_record():
    """学生选课记录页面"""
    stu = session.get("stu")
    if stu is None:
        return render_template("page404.html"), 404

    selcourse_li = SelcourseManage.get_by_sid(stu.id)
    return render_template("student/course_record.html", selcourse_li=selcourse_li)


@app_stu.route("/selCoursePage", methods=["POST", "GET"])
def sel_course_page():
    """选课操作页面"""
    stu = session.get("stu")
    if stu is None:
        return render_template("page404.html"), 404

    if RedisService.judge_can_sel(stu) is False:
        return render_template("not_allow.html", message="不在选课时段，无法进行选课和退选...")

    crd_sum = StuService.count_credit(stu.id)
    if crd_sum >= 33:
        return render_template("not_allow.html", message="所修学分已满，不需要选课...")

    data = request.form
    page = int(data.get("page", request.args.get("page", 1)))
    caid = stu.caid
    ctype = data.get("ctype", session.get("ctype", "all"))
    week = data.get("week", session.get("week", "all"))
    session["caid"] = caid
    session["ctype"] = ctype
    session["week"] = week

    course_li, sum, pagenum, page = StuService.get_preview_course(caid, ctype, week, page, 4)
    preview_li = StuService.get_predone(stu.sno)
    sel_li = SelcourseManage.get_by_sidnoend(stu.id)

    return render_template("student/sel_course.html",
                           course_li=course_li,
                           preview_li=preview_li,
                           sel_li=sel_li,
                           page=page,
                           pagenum=pagenum,
                           sum=sum)


@app_stu.route("/selCourse", methods=["POST"])
def sel_course():
    """选课提交操作"""
    stu = session.get("stu")
    if stu is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    sel_li = request.form.get("sel_li").split(",")

    bl, cids = StuService.save_sel_course(stu.id, stu.sno, stu.caid, sel_li)
    if bl:
        return jsonify({
            "tip": cids,
            "bl": 200
        })
    else:
        return jsonify({
            "tip": cids,
            "bl": 400
        })


@app_stu.route("/selRemove", methods=["POST"])
def sel_remove():
    """退选课操作"""
    stu = session.get("stu")
    if stu is None:
        return jsonify({
            "tip": "账号已下线，请重新登录！"
        })

    cid = request.form.get("cid")
    bl, tip = StuService.remove_sel_course(stu.id, stu.sno, cid, stu.caid)
    if bl:
        return jsonify({
            "bl": 200,
            "tip": tip
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": tip
        })

