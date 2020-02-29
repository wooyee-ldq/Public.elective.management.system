# coding:utf-8


class Msghiden(object):

    @staticmethod
    def pid_hide(pid):
        new_pid = ""
        i = 0
        for s in str(pid):
            i += 1
            if i > 6:
                new_pid = new_pid + "*"
            else:
                new_pid = new_pid + s

        return new_pid

    @classmethod
    def is_hide(cls, pid):
        i = 0
        for s in str(pid):
            i += 1
            if i > 6 and "*" == s:
                return False

        return True

