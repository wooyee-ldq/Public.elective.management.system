# # coding:utf-8
#
#
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, EqualTo, Length
#
#
# class LoginForm(FlaskForm):
#     """自定义管理员登录表单"""
#     username = StringField(label=u"@", validators=[DataRequired("用户名不能为空！")])
#     password = PasswordField(label=u"#", validators=[DataRequired("密码不能为空")])
#     submit = SubmitField(label=u"登录")
