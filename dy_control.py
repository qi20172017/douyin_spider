# !/usr/bin/env python
# coding:utf-8
# Time:2019/9/27 14:56
# write_by:QiFuMin
# script_name:douyin3dazhuang.py
import time
from dy_handle_id import Handle_id
import dy_setting
from dy_init import Init
from dy_cont import Count


class Search():
	def __init__(self, d):
		self.d = d

	# 搜素页面
	def search_screen(self):
		self.search_cont_add_judge()
		user_id = Handle_id.get_user_id()
		Init.update(self.d)
		# 点击输入框
		self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/al0"]').click()
		time.sleep(0.4)
		self.d.send_keys(user_id, clear=True)
		print('Enter ID:' + user_id)
		time.sleep(0.5)
		if self.d.xpath('//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').wait(10):
			self.search_case_two()
		else:
			self.search_case_one()

		if self.d.xpath('//*[@text="用户"]').wait(10):
			Init.update(self.d)
			self.d.xpath('//*[@text="用户"]').click()
			print('Click on the “用户”')
			time.sleep(0.5)
			if self.d.xpath(
			'//*[@resource-id="com.ss.android.ugc.aweme:id/bm0"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]').wait(
			timeout=20):
				self.persion_card(user_id)
			else:
				self.no_user(user_id)
		else:
			Handle_id.save_error_id(user_id)
			self.search_screen()

	def no_user(self, user_id):
		print('根据ID找不到用户')
		Handle_id.save_error_id(user_id)
		self.d.press("back")
		time.sleep(1)
		self.search_screen()

	def search_cont_add_judge(self):
		add_one = Count.get_search_cont()
		if add_one > dy_setting.search_page_num:
			Count.update_search_cont(0)
			Init.back_again(self.d)
		else:
			add_one += 1
			Count.update_search_cont(add_one)

	# 如果输入法出现，直接点搜索
	def search_case_one(self):
		time.sleep(0.5)
		# 点击第一个搜索结果
		# d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/cq7"]/android.widget.LinearLayout[1]').click()
		self.d.click(0.912, 0.954)

	# 调出输入法
	def search_case_two(self):
		time.sleep(1)
		self.d.click(0.857, 0.974)
		time.sleep(0.8)
		self.d.xpath(
			'//*[@resource-id="android:id/select_dialog_listview"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/com.letv.leui.widget.LeCheckBox[1]').click()
		time.sleep(0.8)
		self.d.click(0.912, 0.954)

	def persion_card(self, user_id):

		self.d.xpath(
			'//*[@resource-id="com.ss.android.ugc.aweme:id/bm0"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]').click(
			timeout=30)
		print('Click on personal business card')
		# 判断是否是私密账号
		print('进入个人中心了，等待数据，然后判断下是都是私密号')
		if self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/title"]').wait(15):
			self.secret(user_id)
		else:
			# 判断是否加载出了内容
			if self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/an1"]').wait(15):
				# 先判断需不需要更多的id
				if dy_setting.follow_get:
					self.following()
				if dy_setting.video_get:
					self.video()
				self.center_to_search()
			else:
				self.nothing(user_id)

	def nothing(self, user_id):
		Count.center_cont_add()
		time.sleep(0.5)
		if Count.get_center_cont() > dy_setting.persion_center_num:
			Count.update_center_cont(0)
			self.center_to_search()
		else:
			self.d.press("back")
			time.sleep(1)
			self.persion_card(user_id)

	def secret(self, user_id):
		"""
		如果是私密账号，保存私密账号，并去到搜索页
		:param user_id:
		:return:
		"""
		Handle_id.save_secret_id(user_id)
		self.center_to_search()

	def following(self):
		# 点击关注
		self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/an1"]').click()
		print('点击查看关注的人')
		time.sleep(0.5)
		# 判断是否为没有关注任何人
		print('等待加载....')
		if self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/e7y"]').wait(15):
			self.follow_none()
		else:
			print('有关注的人，即将爬取')
			# 判断列表中第一个是否存在
			if self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/cww"]/android.widget.RelativeLayout[1]').wait(10):
				self.follow_up_slide()
			else:
				self.follow_nothing()

	# 网红列表页一直打不开，报错
	def follow_error(self):
		print('页面没有打开，没有获取到给用户关注的人的ID')
		time.sleep(0.5)
		self.d.press("back")

	# 没有关注任何人
	def follow_none(self):
		print('该用户没有关注任何人，退出到个人中心')
		time.sleep(0.5)
		self.d.press("back")

	# 网红列表页一直打不开
	def follow_nothing(self):
		Count.follow_cont_add()
		time.sleep(0.5)
		if Count.get_follow_cont() > dy_setting.follow_page_num:
			Count.update_follow_cont(0)
			self.follow_error()
		else:
			self.d.press("back")
			time.sleep(1)
			self.following()

	def follow_up_slide(self):
		con = 0
		while True:
			con += 1
			Init.up_slide(self.d)
			print('网红上滑第%s次' % con)
			time.sleep(1)
			if con > dy_setting.follow_up_slide_num:
				print('已达到最高上滑次数，退出到个人中心')
				break

			# 判断是否出现没有更多了
			if self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/cww"]/android.widget.FrameLayout[1]').exists:
				time.sleep(0.5)
				# 再次确认真的出现没有更多了吗？
				if self.d.xpath(
						'//*[@resource-id="com.ss.android.ugc.aweme:id/cww"]/android.widget.FrameLayout[1]').exists:
					print('没有更多了，返回个人中心')
					break
		self.follow_nomore()

	# 网红页面没有更多了
	def follow_nomore(self):
		time.sleep(0.5)
		self.d.press("back")

	def video(self):
		try:
			self.d.xpath('//*[@text="作品"]').click()
			print('点击作品')
		except:
			print('该用户没有其他干扰项，判断作品数')
			pass
		if self.d.xpath('//*[@text="作品 0"]').wait(1):
			print('该用户的作品数为零')
			pass
		else:
			print('一般用户，即将上滑')
			self.video_up_slide()

	def video_up_slide(self):
		con = 0
		while True:
			con += 1
			Init.up_slide(self.d)
			print('视频上滑第%s次' % con)
			time.sleep(1)
			if con > dy_setting.video_up_slide_num:
				print('已达到最大上滑次数，已停止')
				break

			# 判断是否出现没有更多了
			if self.d.xpath('//*[@text="暂时没有更多了"]').exists:
				time.sleep(0.5)
				# 再次确认真的出现没有更多了吗？
				if self.d.xpath('//*[@text="暂时没有更多了"]').exists:
					print("没有更多视频了，已停止")
					break
		self.video_nomore()

	def video_nomore(self):
		time.sleep(0.5)
		# d.press("back")
		# 这已经是个人中心了

	# 从个人中心返回到搜索页面
	def center_to_search(self):
		time.sleep(0.5)
		self.d.press("back")
		print('退出到搜索结果页面')
		time.sleep(0.5)
		self.d.press("back")
		print('退出到搜索页面')
		time.sleep(0.5)
		self.search_screen()

	@staticmethod
	def dayin():
		print('778899')


if __name__ == '__main__':
	Init.init_device_db()
	devices = Init.connection()
	Init.start_dy(devices)
	Init.search_box(devices)
	search = Search(devices)
	# aaa.start_dy()
	time.sleep(10)
	search.search_screen()
	# time.sleep(3)
	# Start.back_again(devices)