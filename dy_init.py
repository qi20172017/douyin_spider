# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/14 23:34
# write_by:QiFuMin
# script_name:dy_init.py

import dy_setting
import time
import uiautomator2 as u2
from dy_cont import Count
import os


class Init():
	@staticmethod
	def init_device_db():
		# 初始化手机，还有数据库中的三个计数器
		Count.update_search_cont(0)
		Count.update_follow_cont(0)
		Count.update_center_cont(0)
		if dy_setting.init_devices:
			print('开始初始化设备....')
			os.system('python -m uiautomator2 init')
		else:
			print('初始化设备功能没有打开')

	@staticmethod
	def connection():
		d = u2.connect(dy_setting.device_name)
		return d
	# 启动抖音app
	@staticmethod
	def start_dy(d):
		d.app_start("com.ss.android.ugc.aweme")

	@staticmethod
	def search_box(d):
		time.sleep(20)
		Init.update(d)
		d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/akt"]').click(timeout=600)
		print('Locate to the search box')
		time.sleep(0.5)
		# search_screen()

	@staticmethod
	def back_again(d):
		time.sleep(0.5)
		d.press("back")
		print('退回主页')
		time.sleep(0.8)
		d.press("back")
		print('再次确认退回主页')
		time.sleep(1.5)
		d.press("back")
		print('退回-一次')
		time.sleep(0.2)
		d.press("back")
		print('退出二次')
		for i in range(dy_setting.back_rest_time):
			time.sleep(1)
			print('休息第%s秒' % i)
		print('启动')
		Init.start_dy(d)
		Init.search_box(d)

	# self.d.xpath(
	# 	'//*[@resource-id="com.android.launcher3:id/workspace"]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[7]').click()

	@staticmethod
	def update(d):
		if d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/dda"]').exists:
			print('检查到更新')
			time.sleep(0.5)
			try:
				d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/bbn"]').click()
				print('点击不更新')
				time.sleep(1.5)
			except:
				pass

		if d.xpath('//*[@text="进入青少年模式"]').exists:
			print('检查到未成年模式')
			time.sleep(0.5)
			try:
				d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/e4z"]').click()
				print('点击不进入')
				time.sleep(1.5)
			except:
				pass

	@staticmethod
	def up_slide(d):
		x1 = 550
		y1 = 1700
		x2 = 500
		y2 = 500
		d.swipe(x1, y1, x2, y2, 0.04)


if __name__ == '__main__':
	pass

