# music_download
## 工程文件说明
整个工程代码主体分为两个部分：
1. kg.py: 下载女神在全民K歌上发布的歌
2. changba.py: 下载女神在唱吧上发布的歌

## 设计场景说明
因为没有写配置文件的原因，所以在初次运行代码的时候最好不要中断。以后再运行都会只下载最新的文件，当然前提是下载目录的文件没有移动。因为文件是按时间递减顺序下载的，如果只下载了前面几个文件，下次运行后面的文件也不会接着下载。最简单直接的方法就是删除已经下载的文件，并重新完整地运行程序即可。

## 使用方法说明
对应的.py文件我都写了个简单的批处理文件，只要双击即可运行。前提是你已经安装好了Python环境以及相应的库文件。
