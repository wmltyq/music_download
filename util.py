import os, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}


# 判断存储路径是否存在
def dir_exist(path):
    if os.path.exists(path):
        print('“' + path + '”文件路径已创建')
    else:
        os.makedirs(path)
        print('“' + path + '”文件路径创建成功')


# 判断音频是否已经下载
def file_exist(file):
    if os.path.exists(file):
        print('>>> 已下载全部最新\n')
        return True
    return False


# 验证文件名合法性
def verify_file_name(file_name):
    return re.sub('[\/:*?"<>|]', '', file_name)
