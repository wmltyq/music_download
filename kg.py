import requests, re, json, urllib
from bs4 import BeautifulSoup
from util import file_exist, dir_exist, headers, verify_file_name


def download_img_audio(shareids, path):
    for shareid in shareids:
        # 构建歌曲URL
        url = 'http://node.kg.qq.com/play?s=' + shareid
        # 根据歌曲链接依次下载
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        script_tag = soup.find_all('script', text=re.compile('window.__DATA__'))
        tag_data = script_tag[0].text.replace('window.__DATA__ = ', '').replace(';', '')
        dict_data = json.loads(tag_data)
        # 歌曲名
        song_name = dict_data['detail']['song_name']
        # 音频链接
        play_url = dict_data['detail']['playurl']
        # 歌曲封面
        cover = dict_data['detail']['cover']
        # 正则表达式去除非法字符，不然以此作为文件名会报错
        right_song_name = verify_file_name(song_name)
        m4a_path = path + right_song_name + '.m4a'
        jpg_path = path + right_song_name + '.jpg'
        # 如果歌曲文件已下载则退出当前循环
        if file_exist(m4a_path):
            return True
        print(right_song_name)
        print('>>> ' + play_url)
        urllib.request.urlretrieve(play_url, m4a_path)
        # 如果专辑图片已下载则退出当前循环
        if file_exist(jpg_path):
            return True
        urllib.request.urlretrieve(cover, jpg_path)
        print('>>> 下载成功')


# 获取一个页面的歌曲列表
def get_shareids(url):
    req = requests.get(url, headers=headers)
    res = req.text
    json_data = json.loads(re.findall(r'^\w+\((.*)\)$', res)[0])
    # 标志是否还有歌曲：1表示还有歌曲，0表示没有歌曲
    has_more = json_data['data']['has_more']
    shareids = []
    for shareid in json_data['data']['ugclist']:
        shareids.append(shareid['shareid'])
    return shareids, has_more


# 一个请求一个请求地下载
def one_by_one(base_url, uid, path):
    start = 1
    shareids, has_more = get_shareids(base_url % (start, uid))
    if download_img_audio(shareids, path):
        return
    while True:
        if has_more == 1:
            start += 1
            shareids, has_more = get_shareids(base_url % (start, uid))
            if download_img_audio(shareids, path):
                break
        else:
            break


if __name__ == '__main__':
    # 请求数据的初始URL, start=1: 表示分页的第1页, num=8: 表示一次请求返回8条数据, share_uid=: 表示用户ID
    base_url = 'http://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?type=get_ugc&start=%s&num=8&share_uid=%s'
    # 全民K歌上叶莉的主页
    # url = 'http://node.kg.qq.com/personal?uid=639d9a83252b3f83'
    # 全民K歌上乔丽的主页
    # url = 'http://node.kg.qq.com/personal?uid=639f9a802224368e30'
    # 叶莉的ID
    yeli_id = '639d9a83252b3f83'
    # 乔丽的ID
    qiaoli_id = '639f9a802224368e30'
    # 歌曲的存储路径
    # yeli_path = 'E:\\Audio\\叶莉\\全民K歌\\'
    yeli_path = './叶莉/全民K歌/'
    # qiaoli_path = 'E:\\Audio\\乔丽\\全民K歌\\'
    qiaoli_path = './乔丽/全民K歌/'

    dir_exist(yeli_path)
    one_by_one(base_url, yeli_id, yeli_path)
    dir_exist(qiaoli_path)
    one_by_one(base_url, qiaoli_id, qiaoli_path)
