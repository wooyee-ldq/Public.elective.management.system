# coding:utf-8


from flask import Flask, session, request, render_template
from redis import Redis
from flask_session import Session
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from Model.myModelView import AdminsModelView, StudentsModelView, \
    SelcoursesModelView, TeachersModelView, AchievementsModelView, \
    ClassesModelView, CollegesModelView, CoseltimeModelView, \
    CoursesModelView, NoticesModelView, CampusesModelView, ClassroomsModelView, LevelsModelView
from flask_babelex import Babel


# 创建Flask应用对象
app = Flask(__name__)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy()


# app的定义配置类
class Config(object):
    # 配置数据库参数【sqlalchemy参数】
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/pecms"
    # 设置sqlalchemy自动跟踪数据库：
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 设置使用flask-session来通过redis保存session数据
    SESSION_TYPE = 'redis'   # session存储格式为redis
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379)  # 配置redis服务器参数
    SESSION_USE_SIGNER = True  # 是否强制加盐，混淆session
    SECRET_KEY = str(uuid.uuid1())  # 如果加盐，那么必须设置的安全码，盐
    SESSION_PERMANENT = False  # session是否长期有效，false，则关闭浏览器，session失效
    PERMANENT_SESSION_LIFETIME = 3600  # session长期有效，则设定session生命周期，整数秒


# 应用配置类
app.config.from_object(Config)

# 配置flask_session
Session(app)

admin = Admin(
    app,
    name='数据表操作台',
    url="/adminConsole",
    template_mode='bootstrap3'
)


# 设置数据表管理台中文显示
babel = Babel(app)
@babel.localeselector
def get_locale():
    # if request.args.get('lang'):
    #     session['lang'] = request.args.get('lang')
    # return session.get('lang', 'en')
    return "zh_CN"


# 过滤所有请求，设置后台管理权限
@app.before_request
def admin_console_examine():
    url = request.path
    if url.split("/")[1] == "adminConsole":
        user = session.get("admin")
        if user is None:
            return render_template("page404.html"), 404
        if user.issuper == 0:
            return "无权限使用该功能，请使用超级管理员身份"


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template("page404.html"), 404


def add_model_view():
    from Model.model import Admins, Students, Teachers, \
        Selcourses, Courses, Coseltime, Achievements,\
        Notices, Classes, Colleges, Campuses, Classrooms, Levels

    # 添加后台管理视图模型
    admin.add_view(AdminsModelView(Admins, db.session, name="管理员表"))
    admin.add_view(StudentsModelView(Students, db.session, name="学生表"))
    admin.add_view(TeachersModelView(Teachers, db.session, name="教师表"))
    admin.add_view(SelcoursesModelView(Selcourses, db.session, name="选课记录表"))
    admin.add_view(CoursesModelView(Courses, db.session, name="课程表"))
    admin.add_view(CoseltimeModelView(Coseltime, db.session, name="开课设置表"))
    admin.add_view(AchievementsModelView(Achievements, db.session, name="成绩表"))
    admin.add_view(NoticesModelView(Notices, db.session, name="公告表"))
    admin.add_view(ClassesModelView(Classes, db.session, name="班级表"))
    admin.add_view(CollegesModelView(Colleges, db.session, name="学院表"))
    admin.add_view(CampusesModelView(Campuses, db.session, name="校区表"))
    admin.add_view(LevelsModelView(Levels, db.session, name="年级表"))
    admin.add_view(ClassroomsModelView(Classrooms, db.session, name="教室表"))


# def register():
#     """全部蓝图注册和路由加入"""
#     from Admin import app_admin
#     from Teacher import app_tea
#     from Student import app_stu
#     # 注册各个模块的蓝图对象
#     app.register_blueprint(app_admin, url_prefix="/admin")
#     app.register_blueprint(app_tea, url_prefix="/tea")
#     app.register_blueprint(app_stu, url_prefix="/stu")


def admin_register():
    from Admin import app_admin
    # 注册管理员模块的蓝图对象
    app.register_blueprint(app_admin, url_prefix="/admin")


def tea_register():
    from Teacher import app_tea
    # 注册教师模块的蓝图对象
    app.register_blueprint(app_tea, url_prefix="/tea")


def stu_register():
    from Student import app_stu
    # 注册学生模块的蓝图对象
    app.register_blueprint(app_stu, url_prefix="/stu")


@app.route("/")
def nav_index():
    """登录导航页面"""
    return render_template("nav_index.html"), 200


def run():
    admin_register()
    tea_register()
    stu_register()
    db.init_app(app)  # 通过flask的app应用加入数据库配置
    add_model_view()
    print(app.url_map)
    print("http://127.0.0.1:2333")
    print("http://127.0.0.1:2333/admin")
    print("http://127.0.0.1:2333/stu")
    print("http://127.0.0.1:2333/tea")
    app.run(host="127.0.0.1", port=2333, debug=True)  # 默认是运行在5000端口


if __name__ == "__main__":
    run()




