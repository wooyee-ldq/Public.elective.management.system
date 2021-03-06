# coding:utf-8


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """自定义登录表单"""
    username = StringField(label=u"用户", validators=[DataRequired("用户名不能为空！")])
    password = PasswordField(label=u"密码", validators=[DataRequired("密码不能为空!"), Length(6, 32, "密码长度在6-32位！")])
    submit = SubmitField(label=u"登录")

