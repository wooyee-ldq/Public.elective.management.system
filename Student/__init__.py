# coding:utf-8


from flask import Blueprint


# 创建admin模块的蓝图对象
app_stu = Blueprint("app_stu", __name__)


from .route import *
