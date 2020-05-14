# coding:utf-8


from Tool.encryption import Encryption
from sqlalchemy.dialects.mysql import \
    CHAR, DATE, DATETIME, FLOAT, INTEGER, SMALLINT, TIME, TINYINT, VARCHAR, TEXT
from main import db
import pymysql
pymysql.install_as_MySQLdb()  # python3要执行该配置


# # 创建数据库sqlalchemy工具对象
# db = SQLAlchemy(app)


# 创建模型类
class Admins(db.Model):
    """管理员表模型类"""
    __tablename__ = "admins"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    ano = db.Column(INTEGER, unique=True, nullable=False)  # 账号
    password = db.Column(CHAR(32), nullable=False)  # 密码
    pwd = db.Column(VARCHAR(32), nullable=False)  # 初始密码
    issuper = db.Column(TINYINT(1), nullable=False)  # 超级管理员标志
    examine = db.Column(TINYINT(1), nullable=False)  # 课程审批权限标志

    def set_pwd(self, pwd):
        self.password = Encryption.md5(pwd)

    def __repr__(self):
        return str(self.ano)


class Classes(db.Model):
    """班级表模型类"""
    __tablename__ = "classes"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    clname = db.Column(VARCHAR(30), nullable=False)  # 班级名称

    lid = db.Column(INTEGER, db.ForeignKey("levels.id"))  # 年级id
    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 校区id
    collid = db.Column(INTEGER, db.ForeignKey("colleges.id"))  # 班级所属学院id

    students = db.relationship("Students", backref="classes")

    def __repr__(self):
        return self.clname


class Campuses(db.Model):
    """校区表模型类"""
    __tablename__ = "campuses"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    caname = db.Column(VARCHAR(20), unique=True, nullable=False)  # 校区名称

    classes = db.relationship("Classes", backref="campus")
    colleges = db.relationship("Colleges", backref="campus")
    teachers = db.relationship("Teachers", backref="campus")
    students = db.relationship("Students", backref="campus")
    classrooms = db.relationship("Classrooms", backref="campus")
    courses = db.relationship("Courses", backref="campus")
    coseltimes = db.relationship("Coseltime", backref="campus")

    def __repr__(self):
        return self.caname


class Colleges(db.Model):
    """学院表模型类"""
    __tablename__ = "colleges"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    collname = db.Column(VARCHAR(50), nullable=False)  # 学院名称

    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 校区id

    classes = db.relationship("Classes", backref="college")
    teachers = db.relationship("Teachers", backref="college")
    students = db.relationship("Students", backref="college")

    def __repr__(self):
        return self.collname


class Classrooms(db.Model):
    """教室表模型类"""
    __tablename__ = "classrooms"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    rname = db.Column(INTEGER, nullable=False)  # 教室号
    building = db.Column(TINYINT, nullable=False)  # 教学楼号
    floor = db.Column(TINYINT, nullable=False)  # 楼层号
    numb = db.Column(TINYINT, nullable=False)  # 教室层序号

    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 校区id

    courses = db.relationship("Courses", backref="classroom")

    def __repr__(self):
        return str(self.rname)


class Courses(db.Model):
    """课程表模型类"""
    __tablename__ = "courses"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    cname = db.Column(VARCHAR(30), nullable=False)  # 课程名称
    ctype = db.Column(VARCHAR(10), nullable=False)  # 课程类型
    classweek = db.Column(CHAR(3), nullable=False)  # 上课星期
    classtime = db.Column(TIME, nullable=False)  # 上课时间
    cnum = db.Column(SMALLINT, nullable=False)  # 上课最大人数
    cretime = db.Column(DATETIME, nullable=False)  # 课程创建时间
    updtime = db.Column(DATETIME, nullable=False)  # 课程修改/审批时间
    credit = db.Column(TINYINT, nullable=False)  # 学分
    ispass = db.Column(TINYINT(1), nullable=False, default=0)  # 是否通过审批
    isexamine = db.Column(TINYINT(1), nullable=False, default=0)  # 是否已被审批
    isend = db.Column(TINYINT(1), nullable=False, default=0)  # 课程是否结束标志

    rid = db.Column(INTEGER, db.ForeignKey("classrooms.id"))  # 上课教室id
    tid = db.Column(INTEGER, db.ForeignKey("teachers.id"))  # 课程开设教师id
    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 开课校区id

    selcourses = db.relationship("Selcourses", backref="course")
    achievements = db.relationship("Achievements", backref="course")

    def list_to_dict(self):
        return {
            "id": self.id,
            "cname": self.cname,
            "ctype": self.ctype,
            "week": self.classweek,
            "ctime": str(self.classweek) + str(self.classtime),
            "croom": self.classroom.rname,
            "cnum": self.cnum,
            "credit": self.credit,
            "caname": self.campus.caname,
            "tname": self.teacher.tname,
            "caid": self.caid
        }

    def __repr__(self):
        return self.cname


class Selcourses(db.Model):
    """选课记录表模型类"""
    __tablename__ = "selcourses"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    cretime = db.Column(DATETIME, nullable=False)  # 创建时间

    sid = db.Column(INTEGER, db.ForeignKey("students.id"))  # 选课学生id
    cid = db.Column(INTEGER, db.ForeignKey("courses.id"))  # 课程id

    def __repr__(self):
        return str(self.sid) + ":" + str(self.cid)


class Students(db.Model):
    """学生表模型类"""
    __tablename__ = "students"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    sno = db.Column(INTEGER, unique=True, nullable=False)  # 学号
    sname = db.Column(VARCHAR(20), nullable=False)  # 姓名
    ssex = db.Column(TINYINT(1), nullable=False)  # 性别
    endate = db.Column(DATE, nullable=False)  # 入学日期
    nativeplace = db.Column(VARCHAR(100), nullable=False)  # 籍贯
    birthday = db.Column(DATE, nullable=False)  # 生日
    password = db.Column(CHAR(32), nullable=False)  # 密码
    tel = db.Column(CHAR(11), nullable=False)  # 电话
    degree = db.Column(VARCHAR(20), nullable=False)  # 学位信息
    pid = db.Column(VARCHAR(30), nullable=False)  # 身份证号

    lid = db.Column(INTEGER, db.ForeignKey("levels.id"))  # 年级id
    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 校区id
    collid = db.Column(INTEGER, db.ForeignKey("colleges.id"))  # 学院id
    clid = db.Column(INTEGER, db.ForeignKey("classes.id"))  # 班级id

    selcourses = db.relationship("Selcourses", backref="student")
    achievements = db.relationship("Achievements", backref="student")

    def set_pwd(self, pwd):
        self.password = Encryption.md5(pwd)

    def set_pid(self, pid):
        self.pid = Encryption.base64_encode(pid)

    def __repr__(self):
        return str(self.sno) + ":" + self.sname


class Teachers(db.Model):
    """教师表模型类"""
    __tablename__ = "teachers"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    tno = db.Column(INTEGER, unique=True, nullable=False)  # 账号
    tname = db.Column(VARCHAR(20), nullable=False)  # 姓名
    tsex = db.Column(TINYINT(1), nullable=False)  # 性别
    password = db.Column(CHAR(32), nullable=False)  # 密码
    tel = db.Column(CHAR(11), nullable=False)  # 电话

    collid = db.Column(INTEGER, db.ForeignKey("colleges.id"))  # 所属学院id
    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 所属校区id

    courses = db.relationship("Courses", backref="teacher")

    def set_pwd(self, pwd):
        self.password = Encryption.md5(pwd)

    def __repr__(self):
        return str(self.tno) + ":" + self.tname


class Achievements(db.Model):
    """成绩表模型类"""
    __tablename__ = "achievements"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    grade = db.Column(TINYINT, nullable=False, default=0)  # 分数
    credit = db.Column(TINYINT, nullable=False, default=0)  # 学分
    gradepoint = db.Column(FLOAT, nullable=False, default=0)  # 绩点
    isgreat = db.Column(TINYINT(1), nullable=False, default=-1)  # 成绩是否有效标志

    sid = db.Column(INTEGER, db.ForeignKey("students.id"))  # 学生id
    cid = db.Column(INTEGER, db.ForeignKey("courses.id"))  # 课程id

    def __repr__(self):
        return str(self.grade)


class Coseltime(db.Model):
    """选课时段记录表模型类"""
    __tablename__ = "coseltime"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    cretime = db.Column(DATETIME, nullable=False)  # 创建时间
    updtime = db.Column(DATETIME, nullable=False)  # 更新时间
    starttime = db.Column(DATETIME, nullable=False)  # 开始时间
    endtime = db.Column(DATETIME, nullable=False)  # 结束时间
    remark = db.Column(VARCHAR(100), nullable=False)  # 备注信息
    isend = db.Column(TINYINT(1), nullable=False)  # 是否结束

    lid = db.Column(INTEGER, db.ForeignKey("levels.id"))  # 年级id
    caid = db.Column(INTEGER, db.ForeignKey("campuses.id"))  # 校区id

    def __repr__(self):
        return self.remark


class Levels(db.Model):
    """年级表模型类"""
    __tablename__ = "levels"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    lname = db.Column(VARCHAR(10), unique=True, nullable=False)  # 年级

    classes = db.relationship("Classes", backref="level")
    students = db.relationship("Students", backref="level")
    coseltimes = db.relationship("Coseltime", backref="level")

    def __repr__(self):
        return self.lname


class Notices(db.Model):
    """公告表模型类"""
    __tablename__ = "notices"

    id = db.Column(INTEGER, primary_key=True)  # id主键
    text = db.Column(TEXT, nullable=False)  # 公告内容
    cretime = db.Column(DATETIME, nullable=False)  # 创建时间
    isover = db.Column(TINYINT, nullable=False)  # 是否失效

    def __repr__(self):
        return self.text


# if __name__ == '__main__':
#
#     admin = Admin.query.filter_by(ano=1234567891).first()
#     print(admin)

    # admin1 = Admin(ano=1234567892, password="345678", issuper=0, examine=0)
    # db.session.add(admin1)
    # db.session.commit()


