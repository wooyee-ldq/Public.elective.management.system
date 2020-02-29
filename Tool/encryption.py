# coding:utf-8
import base64
import hashlib


class Encryption(object):
    """md5加密和base64编码解码工具类"""

    @staticmethod
    def md5(s):
        # md5加盐加密
        salt = "%456^123@#$&890()?*"  # 盐字符串
        ss = str(s) + salt
        return hashlib.md5(ss.encode()).hexdigest()  # 加密

    @staticmethod
    def base64_encode(s):  # base64编码
        ss = base64.b64encode(str(s).encode("utf-8")).decode("utf-8")
        return ss

    @staticmethod
    def base64_decode(s):  # base64解码
        ss = base64.b64decode(str(s).encode("utf-8")).decode("utf-8")
        return ss


if __name__ == '__main__':
    s = "1234123402"
    no = Encryption.md5(s)
    print(no)

    pid = Encryption.base64_encode("440973199702102637")
    print(pid)
