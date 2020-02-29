# coding:utf-8
import time


class ExceptionLog(object):

    @staticmethod
    def model_error(log_str):
        file_name = "Log_file/exception_log/model_error/" + time.strftime("%Y-%m-%d-", time.localtime()) + "model_error.log"
        with open(file_name, "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S : ", time.localtime()) + log_str + "\n")

    @staticmethod
    def other_error(log_str):
        file_name = "Log_file/exception_log/other_error/" + time.strftime("%Y-%m-%d-", time.localtime()) + "other_error.log"
        with open(file_name, "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S : ", time.localtime()) + log_str + "\n")

