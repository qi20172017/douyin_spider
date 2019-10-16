# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/15 14:12
# write_by:QiFuMin
# script_name:main.py
import time
import os
from dy_control import Search
from dy_downbideo import Downvideo
from dy_init import Init
from multiprocessing import Process


class Start():

	def start_spider(self):
		Init.init_device_db()
		devices = Init.connection()
		Init.start_dy(devices)
		Init.search_box(devices)
		search = Search(devices)
		# aaa.start_dy()
		time.sleep(10)
		search.search_screen()

	def start_download(self):
		dv = Downvideo()
		dv.start_down()

	def start_filter(self):
		dirname_path = os.path.dirname(os.path.abspath(__file__))
		script_path = dirname_path + '\\' + 'dy_response_filter.py'
		print(script_path)
		command = 'mitmdump -p 8888 -s %s' % script_path
		os.system(command)


if __name__ == '__main__':
	project_start = Start()
	filter = Process(target=project_start.start_filter)
	filter.start()
	# filter.join()

	download = Process(target=project_start.start_download)
	download.start()
	# download.join()

	spider = Process(target=project_start.start_spider)
	spider.start()
	# spider.join()

