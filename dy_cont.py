# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/14 11:02
# write_by:QiFuMin
# script_name:text.py
import MySQLdb
import dy_setting


class Count():
	@staticmethod
	def get_center_cont():
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		# db = MySQLdb.connect("localhost", "root", "369852", "douyin", charset='utf8')
		cursor = db.cursor()
		get_center_sql = "SELECT persion_center_cont FROM cont"
		try:
			cursor.execute(get_center_sql)
			results = cursor.fetchall()
			print('获取个人中心打开次数: %s'%results[0][0])
		except:
			print("获取个人中心打开次数失败")
			db.rollback()
			results = ((),)
		db.close()
		return results[0][0]

	@staticmethod
	def update_center_cont(center_cont):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		cursor = db.cursor()
		update_center_sql = "UPDATE cont SET persion_center_cont=%s"

		try:
			cursor.execute(update_center_sql, (center_cont,))
			print('更新 个人中心 打开次数为：%s'%center_cont)
			db.commit()
		except:
			print('更新 个人中心 打开次数失败')
			db.rollback()

		db.close()

	@staticmethod
	def center_cont_add():
		# 取出来，加一，再放回去
		add_one = Count.get_center_cont()
		add_one += 1
		Count.update_center_cont(add_one)

	@staticmethod
	def get_follow_cont():
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		# db = MySQLdb.connect("localhost", "root", "369852", "douyin", charset='utf8')
		cursor = db.cursor()
		get_follow_sql = "SELECT follow_page_cont FROM cont"
		try:
			cursor.execute(get_follow_sql)
			results = cursor.fetchall()
			print('获取 网红列表页 打开次数: %s'%results[0][0])
		except:
			print("获取 网红列表页 打开次数失败")
			db.rollback()
			results = ()
		db.close()
		return results[0][0]

	@staticmethod
	def update_follow_cont(follow_cont):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		cursor = db.cursor()
		update_follow_sql = "UPDATE cont SET follow_page_cont=%s"

		try:
			cursor.execute(update_follow_sql, (follow_cont,))
			print('更新 网红列表页 打开次数为：%s' % follow_cont)
			db.commit()
		except:
			print('更新 网红列表页 打开次数失败')
			db.rollback()

		db.close()

	@staticmethod
	def follow_cont_add():
		# 取出来，加一，再放回去
		add_one = Count.get_follow_cont()
		add_one += 1
		Count.update_follow_cont(add_one)

	@staticmethod
	def get_search_cont():
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)

		cursor = db.cursor()
		get_search_sql = "SELECT search_page_cont FROM cont"
		try:
			cursor.execute(get_search_sql)
			results = cursor.fetchall()
			print('获取 搜索页面 打开次数: %s' % results[0][0])
		except:
			print("获取 搜索页面 打开次数失败")
			db.rollback()
			results = ((),)
		db.close()
		return results[0][0]

	@staticmethod
	def update_search_cont(search_cont):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		cursor = db.cursor()
		update_search_sql = "UPDATE cont SET search_page_cont=%s"
		try:
			cursor.execute(update_search_sql, (search_cont,))
			print('更新 搜索页面 打开次数为：%s' % search_cont)
			db.commit()
		except:
			print('更新 搜索页面 打开次数失败')
			db.rollback()
		db.close()


if __name__ == '__main__':
	Count.follow_cont_add()


