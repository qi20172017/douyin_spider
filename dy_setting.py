# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/2 10:42
# write_by:QiFuMin
# script_name:setting.py
import random


device_name = "LE67A06340179566"
host = '127.0.0.1'
port = 3306
user = 'root'
password = '369852'
database = 'douyin'
charset = 'utf8'
# 获取关注的人
follow_get = False
# 获取更多的视频
video_get = False
# 是否初始化设备
init_devices = True
#
persion_center_num = 2
follow_page_num = 2
search_page_num = 30

# 关注页面上滑最大次数
follow_up_slide_num = 50
# 视频页面最大上滑次数
video_up_slide_num = 5
# 退出休息时间/s
back_rest_time = 50
user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            ]


def headers():
    user_agent = random.choice(user_agent_list)
    headers={
            'User-Agent': user_agent,
                }
    return headers

"""
一些特殊的账号
001003070209jst  这个没有作品
迪丽热巴  没有关注
0219040WYH   这个是私密账号
03180219.46520   搜索不到

"""