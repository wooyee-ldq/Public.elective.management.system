# coding:utf-8
import time

from Service.teaManage import TeaManage


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(time.time())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1580802619.5242774)))

    # 先转换为时间数组
    timeArray = time.strptime("2020-04-10 13:00:00", "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)