# # coding:utf-8
#
#
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, RadioField
# from wtforms.validators import DataRequired, EqualTo, Length
#
#
# class LoginForm(FlaskForm):
#     """自定义教师和学生登录表单"""
#     username = StringField(label=u"@", validators=[DataRequired("用户名不能为空！")])
#     password = PasswordField(label=u"#", validators=[DataRequired("密码不能为空")])
#     role = RadioField(label=u"role", choices=[("stu", "学生"), ("tea", "教师")], default="stu")
#     submit = SubmitField(label=u"登录")

