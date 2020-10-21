import base64
import os
import sys


def get_account():
    """
    获取账号信息
    """
    if os.path.exists("data.txt"):
        return __read_accounts()
    else:
        print("未找到data.txt, 判断为首次运行, 请接下来依次输入学号密码")
        uid, psw = __append_account()
    return [(uid, psw)]


def __delete_account():
    """
    删除指定用户
    """
    if os.path.exists("data.txt"):
        accounts = __read_accounts()
        for i, (uid, _) in enumerate(accounts):
            print(str(i) + ": " + uid)
        while True:
            n = input("请输入要删除的account序号(-1退出):")
            try:
                n = int(n)
                if 0 <= n < len(accounts):
                    break
                elif n == -1:
                    return
                else:
                    print("请输入正确的数字范围!")
            except ValueError:
                print("请输入数字!")
        accounts.pop(n)
        try:
            with open("temp.txt", "w+") as f:
                for (uid, psw) in accounts:
                    uid_b = base64.b64encode(uid.encode("UTF-8")).decode("UTF-8")
                    psw_b = base64.b64encode(psw.encode("UTF-8")).decode("UTF-8")
                    f.write(uid_b + "\n" + psw_b + "\n")
        except IOError:
            os.remove("temp.txt")
        os.rename("temp.txt", "data.txt")
    else:
        print("未找到data.txt")


def __append_account():
    """
    新增用户
    """
    uid_psws = __read_accounts()
    accounts = [uid for (uid, _) in uid_psws]
    print("追加新的account...")
    uid = input("学号：")
    if uid in accounts:
        print("账号已经存在!")
        return
    psw = input("密码：")
    uid_b = base64.b64encode(uid.encode("UTF-8")).decode("UTF-8")
    psw_b = base64.b64encode(psw.encode("UTF-8")).decode("UTF-8")
    with open("data.txt", "a+") as old:
        old.write(uid_b + "\n" + psw_b + "\n")
    print("账号已保存在目录下data.txt")
    return uid, psw


def __read_accounts():
    """
    读取账号txt为python List
    """
    accounts = []
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as old:
            raw = old.readlines()
        for i in range(0, len(raw), 2):
            uid_b = raw[i].strip()
            uid = base64.b64decode(uid_b).decode("UTF-8")
            psw_b = raw[i + 1].strip()
            psw = base64.b64decode(psw_b).decode("UTF-8")
            accounts.append((uid, psw))
    return accounts


if __name__ == '__main__':
    if len(sys.argv) == 1:
        __append_account()
    else:
        if sys.argv[1] == "delete":
            __delete_account()
        elif sys.argv[1] == "show":
            for j, (stu_id, _) in enumerate(__read_accounts()):
                print(str(j) + ": " + stu_id)
        else:
            print("支持的命令行参数为delete/show")
