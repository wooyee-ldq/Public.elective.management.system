# coding:utf-8


from Service.loginCheck import LoginCheck


if __name__ == '__main__':
    admin = LoginCheck.admin_pwd_check("1234567891", "234567")
    print(admin)


