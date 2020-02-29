# coding:utf-8


from flask import render_template, request, jsonify, session, redirect, url_for

from Service.admin_service import AdminService
from Service.campusManage import CampusManage
from Service.changePwd import ChangePwd
from Service.levelManage import LevelManage
from Service.loginCheck import LoginCheck
from Service.teaManage import TeaManage
from Service.stuManage import StuManage
from Service.courseManage import CourseManage
from Service.adminManage import AdminManage
from Service.noticeManage import NoticeManage
from Service.coseltimeManage import CoseltimeManage
from . import app_admin
from Log.loginLog import LoginLog
from WTF_Form.login_form import LoginForm


@app_admin.before_request
def before_request():
    url = request.path
    if len(url.split("/")) > 3:
        admin = session.get("admin")
        if admin is None:
            return render_template("page404.html"), 404


@app_admin.route("/")
def admin_login():
    """返回管理员登录页面"""
    form = LoginForm()
    return render_template("admin/admin_login.html", form=form)


@app_admin.route("/index", methods=["POST"])  # 限制使用post方法访问
def admin_index():
    """管理员登录用户密码验证处理"""
    data = request.form
    user = data.get("username")
    password = data.get("password")
    ip = request.remote_addr

    if user is None or password is None:
        return render_template("page404.html"), 404  # 防止使用postman等工具进行访问

    admin = LoginCheck.admin_pwd_check(user, password)
    if admin is None:
        # 保存日志
        LoginLog.login_error(LoginLog.admin_log_error(user, ip))
        return render_template("admin/admin_login.html",
                               form=LoginForm(),
                               error="账号或密码错误！")  # 系统提示
    else:
        # 保存session
        # 保存日志
        LoginLog.login_success(LoginLog.admin_log_success(user, ip))

        data = LoginCheck.admin_to_dict(admin)
        # 保存用户session
        session["admin"] = admin
        return render_template("admin/admin_index.html", **data)  # 登录成功返回主页


@app_admin.route("/adminExit")
def admin_exit():
    """退出登录操作"""
    session.pop("admin", None)
    return redirect(url_for("app_admin.admin_login"))


@app_admin.route("/changePwd", methods=["POST"])
def change_pwd():
    """修改密码操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({"tip": "账号已下线，请重新登录！"})

    data = request.form
    old_pwd = data.get("old_pwd")
    new_pwd1 = data.get("new_pwd1")
    new_pwd2 = data.get("new_pwd2")

    bl = ChangePwd.admin_change_pwd(admin.id, old_pwd, new_pwd1, new_pwd2)
    if bl is True:
        return jsonify({"tip": "修改成功！"})
    else:
        return jsonify({"tip": "修改失败！"})


@app_admin.route("/courseApply")
def course_apply():
    """显示申请课程的页面"""
    admin = session.get("admin")
    if admin is None:
        return render_template("page404.html"), 404
    if admin.examine == 0:
        return "无权限使用该功能，请联系超级管理员"

    course_li = CourseManage.get_apply_course()
    if course_li is None:
        course_li = list()
    return render_template("admin/course_apply.html", course_li=course_li)


@app_admin.route("/courseAgree", methods=["POST"])
def course_agree():
    """课程申请同意操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    cid_arr = request.form.get("cid_arr")
    cid_li = cid_arr.split(",")
    bl = AdminService.course_agree(cid_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "审批同意操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "审批同意操作失败！"
        })


@app_admin.route("/courseRefuse", methods=["POST"])
def course_refuse():
    """课程申请拒接操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    cid_arr = request.form.get("cid_arr")
    cid_li = cid_arr.split(",")
    bl = AdminService.course_refuse(cid_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "审批拒绝操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "审批拒绝操作失败！"
        })


@app_admin.route("/courseSetting")
def course_setting():
    """开课时间段设置页面"""
    admin = session.get("admin")
    if admin is None:
        return render_template("page404.html"), 404

    seltime_li = CoseltimeManage.get_all()
    campus_li = CampusManage.get_all()
    level_li = LevelManage.get_all()

    seltime_li.reverse()
    return render_template("admin/course_setting.html",
                           seltime_li=seltime_li,
                           campus_li=campus_li,
                           level_li=level_li
                           )


@app_admin.route("/courseSet", methods=["POST"])
def course_set():
    """开课时间段设置操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    data = request.form
    stime = data.get("stime") + ":00"
    etime = data.get("etime") + ":00"

    bl = AdminService.get_letter(stime, etime)  # 开始时间和结束时间判断
    if not bl:
        return jsonify({
            "bl": 400,
            "tip": "结束时间必须在开始时间和现在时间之后！"
        })

    remark = data.get("remark")
    caid = data.get("caid")
    lid = data.get("lid")

    bl = AdminService.set_seltime(stime, etime, remark, caid, lid)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "开课设置成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "开课设置失败！"
        })


@app_admin.route("/courseOver", methods=["POST"])
def course_over():
    """结束选课时段操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    id_arr = request.form.get("cid_arr")
    id_li = id_arr.split(",")
    bl = AdminService.over_seltime(id_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "结束开课操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "结束开课操作失败！"
        })


@app_admin.route("/permissionSetting")
def permission_setting():
    """超级管理员的功能，审批权限设置页面, 显示各个普通管理员信息"""
    admin = session.get("admin")
    if admin is None:
        return render_template("page404.html"), 404

    p = admin.issuper
    if p == 1:
        admin_li = AdminManage.get_all()
        return render_template("admin/permission_setting.html", admin_li=admin_li)

    return "无权限使用该功能"


@app_admin.route("/permissionAgree", methods=["POST"])
def permission_agree():
    """审批权限设置同意操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })
    id_arr = request.form.get("cid_arr")
    id_li = id_arr.split(",")

    bl = AdminManage.permission_agree(id_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "授权操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "授权操作失败！"
        })


@app_admin.route("/permissionRefuse", methods=["POST"])
def permission_refuse():
    """审批权限设置拒绝操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    id_arr = request.form.get("cid_arr")
    id_li = id_arr.split(",")

    bl = AdminManage.permission_refuse(id_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "撤销权限操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "撤销权限操作失败！"
        })


@app_admin.route("/createAdmin", methods=["POST"])
def create_admin():
    """创建普通管理员"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({"tip": "账号已下线，请重新登录！"})
    if admin.issuper == 0:
        return jsonify({"tip": "无权限操作！"})
    username = request.form.get("username")
    password = request.form.get("password")

    bl = AdminManage.add(username, password)
    if bl is True:
        return jsonify({"tip": "创建成功！"})
    else:
        return jsonify({"tip": "创建失败！"})


@app_admin.route("/fastCreateAdmin", methods=["POST"])
def fast_create_admin():
    """快速创建普通管理员"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({"tip": "账号已下线，请重新登录！"})
    if admin.issuper == 0:
        return jsonify({"tip": "无权限操作！"})
    bl = AdminManage.fast_add()
    if bl is True:
        return jsonify({"tip": "创建成功！"})
    else:
        return jsonify({"tip": "创建失败！"})


@app_admin.route("/issueNotice", methods=["POST"])
def issue_notice():
    """发布公告操作"""
    admin = session.get("admin")
    if admin is None:
        return jsonify({"tip": "账号已下线，请重新登录！"})

    notice = request.form.get("notice")

    bl = NoticeManage.add(notice)
    if bl is True:
        return jsonify({"tip": "发布成功！"})
    else:
        return jsonify({"tip": "发布失败！"})


@app_admin.route("/noticeManage")
def notice_manage():
    """公告管理页面"""
    admin = session.get("admin")
    if admin is None:
        return render_template("page404.html"), 404

    notice_li = NoticeManage.get_all()
    return render_template("admin/notice_manage.html", notice_li=notice_li)


@app_admin.route("/noticeOver", methods=["POST"])
def notice_over():
    admin = session.get("admin")
    if admin is None:
        return jsonify({
            "bl": 400,
            "tip": "账号已下线，请重新登录！"
        })

    id_arr = request.form.get("cid_arr")
    id_li = id_arr.split(",")

    bl = NoticeManage.update_over(id_li)
    if bl is True:
        return jsonify({
            "bl": 200,
            "tip": "过期设置操作成功！"
        })
    else:
        return jsonify({
            "bl": 400,
            "tip": "过期设置操作失败！"
        })


#
# @app_admin.route("/teaManage")
# def tea_manage():
#     """显示教师信息的教师管理页面"""
#     admin = session.get("admin")
#     if admin is None:
#         return render_template("page404.html"), 404
#
#     tea_li = TeaManage.get_all()
#     return render_template("admin/tea_manage.html", tea_li=tea_li)  # 返回教师管理页面信息
#
#
# @app_admin.route("/stuManage")
# def stu_manage():
#     """显示学生信息的学生管理页面"""
#     admin = session.get("admin")
#     if admin is None:
#         return render_template("page404.html"), 404
#
#     stu_li = StuManage.get_all()
#     return render_template("admin/stu_manage.html", stu_li=stu_li)  # 返回学生管理页面信息
#
#
# @app_admin.route("/teaAdd", methods=["POST"])
# def tea_add():
#     """教师添加操作"""
#     data = request.form
#     tno = data.get("tno")
#     tname = data.get("tname")
#     tsex = data.get("tsex")
#     collegename = data.get("collegename")
#     password = data.get("password")
#     tel = data.get("tel")
#
#     # 该方法返回布尔值
#     bl = TeaManage.add(
#         tno,
#         tname,
#         tsex,
#         collegename,
#         password,
#         tel
#     )
#
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/teaDel", methods=["POST"])
# def tea_del():
#     """教师删除操作"""
#     tid = request.form.get("tid")
#     bl = TeaManage.delete(tid)
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/teaChange", methods=["POST"])
# def tea_change():
#     """教师信息修改操作"""
#     data = request.form
#     tid = data.get("tid")
#     tno = data.get("tno")
#     tname = data.get("tname")
#     tsex = data.get("tsex")
#     collegename = data.get("collegename")
#     tel = data.get("tel")
#     bl = TeaManage.update(tid, tno, tname, tsex, collegename, tel)
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#     })

#
# @app_admin.route("/teaGet", methods=["POST"])
# def tea_get():
#     """各种筛选获取教师信息"""
#     data = request.form
#     key = data.get("key")
#     value = data.get("value")
#
#     if "tid" == key:
#         tea = TeaManage.get_by_id(value)
#         return jsonify(tea)
#     elif "tname" == key:
#         tea_li = TeaManage.get_by_name(value)
#         return jsonify(tea_li)
#     elif "collegename" == key:
#         tea_li = TeaManage.get_by_college(value)
#         return jsonify(tea_li)
#
#
# @app_admin.route("/stuAdd", methods=["POST"])
# def stu_add():
#     """学生添加操作"""
#     data = request.form
#
#     sno = data.get("sno")
#     sname = data.get("sname")
#     ssex = data.get("ssex")
#     collegename = data.get("collegename")
#     classname = data.get("classname")
#     endate = data.get("endate")
#     nativeplace = data.get("nativeplace")
#     birthday = data.get("birthday")
#     password = data.get("password")
#     tel = data.get("tel")
#     campus = data.get("campus")
#     degree = data.get("degree")
#     pid = data.get("pid")
#
#     bl = StuManage.add(
#         sno,
#         sname,
#         ssex,
#         collegename,
#         classname,
#         endate,
#         nativeplace,
#         birthday,
#         password,
#         tel,
#         campus,
#         degree,
#         pid
#     )
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#     })
#
#
# @app_admin.route("/stuDel", methods=["POST"])
# def stu_del():
#     """学生删除操作"""
#     sid = request.form.get("sid")
#     bl = StuManage.delete(sid)
#
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#     })
#
#
# @app_admin.route("/stuChange", methods=["POST"])
# def stu_change():
#     """学生信息修改操作"""
#     data = request.form
#     sid = data.get("sid")
#     sno = data.get("sno")
#     sname = data.get("sname")
#     ssex = data.get("ssex")
#     collegename = data.get("collegename")
#     classname = data.get("classname")
#     endate = data.get("endate")
#     nativeplace = data.get("nativeplace")
#     birthday = data.get("birthday")
#     tel = data.get("tel")
#     campus = data.get("campus")
#     degree = data.get("degree")
#     pid = data.get("pid")
#
#     bl = StuManage.update(sid, sno, sname, ssex, collegename, classname,
#                           endate, nativeplace, birthday, tel, campus, degree, pid)
#
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/stuGet", methods=["POST"])
# def stu_get():
#     """各种筛选获取学生信息"""
#     data = request.form
#     key = data.get("key")
#     value = data.get("value")
#
#     if "sid" == key:
#         stu = StuManage.get_by_id(value)
#         return jsonify(stu)
#
#     elif "sname" == key:
#         stu_li = StuManage.get_by_name(value)
#         return jsonify(stu_li)
#
#     elif "collegename" == key:
#         stu_li = StuManage.get_by_college(value)
#         return jsonify(stu_li)
#
#     elif "classname" == key:
#         stu_li = StuManage.get_by_class(value)
#         return jsonify(stu_li)
#
#     elif "endate" == key:
#         stu_li = StuManage.get_by_endate(value)
#         return jsonify(stu_li)
#
#     elif "campus" == key:
#         stu_li = StuManage.get_by_campus(value)
#         return jsonify(stu_li)
#
#     elif "degree" == key:
#         stu_li = StuManage.get_by_degree(value)
#         return jsonify(stu_li)



# @app_admin.route("/courseManage")
# def course_manage():
#     """显示课程信息的课程管理页面"""
#     admin = session.get("admin")
#     if admin is None:
#         return render_template("page404.html"), 404
#
#     course_li = CourseManage.get_all()
#     return render_template("admin/course_manage.html", course_li=course_li)
#
#
# @app_admin.route("/courseAdd", methods=["POST"])
# def course_add():
#     """课程添加操作"""
#     data = request.form
#     cname = data.get("cname")
#     ctype = data.get("ctype")
#     classweek = data.get("classweek")
#     classtime = data.get("classtime")
#     classplace = data.get("classplace")
#     tid = data.get("tid")
#     credit = data.get("credit")
#
#     bl = CourseManage.add(cname, ctype, classweek, classtime, classplace, tid, credit)
#
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/courseDel", methods=["POST"])
# def course_del():
#     """课程删除操作"""
#     cid = request.form.get("cid")
#
#     bl = CourseManage.delete(cid)
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/courseChange", methods=["POST"])
# def course_change():
#     """课程修改操作"""
#     data = request.form
#     cid = data.get("cid")
#     cname = data.get("cname")
#     ctype = data.get("ctype")
#     classweek = data.get("classweek")
#     classtime = data.get("classtime")
#     classplace = data.get("classplace")
#     tid = data.get("tid")
#     credit = data.get("credit")
#
#     bl = CourseManage.update(cid, cname, ctype, classweek, classtime, classplace, tid, credit)
#     if bl is True:
#         return jsonify({
#             "bl": 200
#         })
#     else:
#         return jsonify({
#             "bl": 400
#         })
#
#
# @app_admin.route("/courseGet", methods=["POST"])
# def course_get():
#     """各种筛选获取课程信息"""
#     data = request.form
#     key = data.get("key")
#     value = data.get("value")
#
#     if "cid" == key:
#         course = CourseManage.get_by_id(value)
#         return jsonify(course)
#
#     elif "cname" == key:
#         course_li = CourseManage.get_by_name(value)
#         return jsonify(course_li)
#
#     elif "ctype" == key:
#         course_li = CourseManage.get_by_type(value)
#         return jsonify(course_li)
#
#     elif "classweek" == key:
#         course_li = CourseManage.get_by_week(value)
#         return jsonify(course_li)
#
#     elif "classtime" == key:
#         course_li = CourseManage.get_by_time(value)
#         return jsonify(course_li)
#
#     elif "classplace" == key:
#         course_li = CourseManage.get_by_place(value)
#         return jsonify(course_li)
#
#     elif "ispass" == key:
#         course_li = CourseManage.get_by_pass(value)
#         return jsonify(course_li)
#
#     elif "isexamine" == key:
#         course_li = CourseManage.get_by_examine(value)
#         return jsonify(course_li)
#
#     elif "tid" == key:
#         course_li = CourseManage.get_by_tid(value)
#         return jsonify(course_li)
#
#     elif "credit" == key:
#         course_li = CourseManage.get_by_credit(value)
#         return jsonify(course_li)