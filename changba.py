import requests, re, urllib
from bs4 import BeautifulSoup
from util import file_exist, dir_exist, headers, verify_file_name


# 从主页获取每首歌的URL
def get_music_url(user_url):
    req = requests.get(user_url, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    work_list = soup.find_all('li', class_='userPage-work-li')
    music_url = []
    for item in work_list:
        music_url.append(item.find('a')['href'])
    return music_url


def download(music_url, path):
    for url in music_url:
        url = 'http://changba.com' + url
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        # FIXED: 去除文件名后一个空格
        title = soup.find('div', class_='title').get_text().strip()
        # 因为audio的src属性是通过js动态生成的，所以此方法行不通
        # audio = soup.find('audio')['src']
        # 直接从js中提取
        audio = re.search('http://(.*?)\.mp3', html).group()
        # 验证文件名是否正确
        title = verify_file_name(title)
        file = path + title + '.mp3'
        if file_exist(file):
            break
        print(title)
        print('>>> ' + audio)
        urllib.request.urlretrieve(audio, file)
        print('>>> 下载成功')


if __name__ == '__main__':
    # 乔丽的主页URL
    user_url = 'http://changba.com/u/193042513'
    # 存储路径
    path = './乔丽/唱吧/'
    music_url = get_music_url(user_url)
    dir_exist(path)
    download(music_url, path)
