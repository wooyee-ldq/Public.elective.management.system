# coding:utf-8
import time


class LoginLog(object):

    @staticmethod
    def login_success(log_str):
        file_name = "Log_file/login_log/login_success/" + time.strftime("%Y-%m-%d-", time.localtime()) + "login_success.log"
        with open(file_name, "a") as f:
            f.write(log_str + "\n")

    @staticmethod
    def login_error(log_str):
        file_name = "Log_file/login_log/login_error/" + time.strftime("%Y-%m-%d-", time.localtime()) + "login_error.log"
        with open(file_name, "a") as f:
            f.write(log_str + "\n")

    @staticmethod
    def admin_log_error(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-admin-user:" + user + "-login_error"

    @staticmethod
    def tea_log_error(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-teacher-user:" + user + "-login_error"

    @staticmethod
    def stu_log_error(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-student-user:" + user + "-login_error"

    @staticmethod
    def admin_log_success(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-admin-user:" + user + "-login_success"

    @staticmethod
    def tea_log_success(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-teacher-user:" + user + "-login_success"

    @staticmethod
    def stu_log_success(user, ip):
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
               "ip:" + ip + \
               "-student-user:" + user + "-login_success"

