# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/15 13:54
# write_by:QiFuMin
# script_name:dy_handle_id.py
import MySQLdb
import dy_setting

class Handle_id():

	@staticmethod
	def save_error_id(error_id):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user,
		                     password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		# db = MySQLdb.connect(host, "root", "369852", "douyin", charset='utf8')
		cursor = db.cursor()
		sql = "INSERT INTO error_id(user_id)  VALUES ( %s )"
		gxsql = "UPDATE user_info SET flg=3 WHERE user_id = %s"
		try:
			cursor.execute(sql, (error_id,))
			print('Save_Error_ID:Success')
			db.commit()
		except:
			print('Save_Error_ID:Error')
			db.rollback()
		try:
			cursor.execute(gxsql, (error_id,))
			print('Updata_Error_ID_flg:Success')
			db.commit()
		except:
			print('Updata_Error_ID_flg:Error')
			db.rollback()
		db.close()

	@staticmethod
	def save_secret_id(secret_id):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user,
		                     password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		# db = MySQLdb.connect("localhost", "root", "369852", "douyin", charset='utf8')
		cursor = db.cursor()
		lcsql = "INSERT INTO secret_id(user_id) VALUES ( %s )"
		gxsql = "UPDATE user_info SET flg=2 WHERE user_id = %s"

		try:
			cursor.execute(lcsql, (secret_id,))
			print('SaveAs_Secret_ID:Success')
			db.commit()
		except:
			print('SaveAs_Secret_ID:Error')
			db.rollback()
		try:
			cursor.execute(gxsql, (secret_id,))
			print('Updata_Secret_ID_flg:Success')
			db.commit()
		except:
			print('Updata_Secret_ID_flg:Error')
			db.rollback()

		db.close()

	@staticmethod
	def get_user_id():
		"""
		取出一个ID与上一个ID对比，如果一样，就标记本ID有误，然后再取一个，并把这个更新到last_id库中
		:return: user_id
		"""

		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user,
		                     password=dy_setting.password,
		                     database=dy_setting.database, charset=dy_setting.charset)
		# db = MySQLdb.connect("localhost", "root", "369852", "douyin", charset='utf8')
		cursor = db.cursor()
		sql = "SELECT * FROM user_info WHERE flg = 0 LIMIT 1 "
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
		except:
			print("Error: unable to fetch data")
			db.rollback()
			results = ()
		user_id = results[0][1]

		last_sql_cx = "SELECT user_id FROM last_id"
		last_sql_gx = "UPDATE last_id SET user_id=%s"
		try:
			cursor.execute(last_sql_cx)
			last_results = cursor.fetchall()
		except:
			print("Error: unable to fetch data")
			db.rollback()
			last_results = ()
		last_id = last_results[0][0]

		if last_id == user_id:
			print('这次的ID与上次相同，保存错误ID，再重新取出')
			Handle_id.save_error_id(user_id)
			try:
				cursor.execute(sql)
				results = cursor.fetchall()
			except:
				print("Error: unable to fetch data")
				db.rollback()
				results = ()
			user_id = results[0][1]
			try:
				cursor.execute(last_sql_gx, (user_id,))
				print('更新一下新取出的ID到last_id')
				db.commit()
			except:
				print('新取出的ID，更新到last_id没有更新成功')
				db.rollback()
		else:
			print('正常新鲜的ID')
			try:
				cursor.execute(last_sql_gx, (user_id,))
				print('日常更新last_id')
				db.commit()
			except:
				print('日常更新last_id失败')
				db.rollback()
		db.close()

		return user_id
