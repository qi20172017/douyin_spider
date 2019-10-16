# !/usr/bin/env python
# coding:utf-8
# Time:2019/9/14 14:24
# write_by:QiFuMin
# script_name:fans.py
import re
import MySQLdb
import dy_setting
import time
import os


def save_error(text):
	file_path = os.path.dirname(os.path.abspath(__file__)) + '\\Error_message'
	try:
		os.makedirs(file_path)
	except:
		print("This folder already exists")
	file_name = file_path + '\\' + str(time.strftime("%Y-%m-%d %H-%M-%S")) + '.txt'
	with open(file_name, 'w', encoding='utf8') as f:
		f.write(text)


def response(flow):
	db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
	                     database=dy_setting.database, charset=dy_setting.charset)
	# db = MySQLdb.connect("localhost", "root", "369852", "douyin", charset='utf8')
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	try:
		# 这个try是应对.text解码失败的情况，只是避开，还不知道怎么解决
		re_text = flow.response.text

		# 判断是否是关注的请求
		if 'aweme/v1/user/following/list/' in flow.request.url:
			# sql = "INSERT INTO USER1(USER_ID) VALUES (%s)"
			sql = "INSERT INTO user_info(nickname, user_id, total_fav, fans_dou, fans_tou, fans_huo, flg) \
			        VALUES ('none', %s, 0, 0, 0, 0, 0)"

			try:
				# result = re.findall('"short_id": ?"(.*?)"|"unique_id": ?"(.*?)"', re_text)
				short_id = re.findall('"short_id": ?"(.*?)"', re_text)
				unique_id = re.findall('"unique_id": ?"(.*?)"', re_text)
				result = short_id + unique_id
				for i in result:
					if (i != '') & (i != '0'):
						# f.write(i + '\n')
						try:
							cursor.execute(sql, (i,))
							db.commit()
							print(i + '新ID已获取')
						except:
							# print('----------------------------------------------------')
							db.rollback()
			except:
				pass
		# 判断是否是个人中心的请求
		if 'snssdk.com/aweme/v1/user/?sec_user_id' in flow.request.url:
			# 把一些nickname干扰项去掉
			re_text = re.sub('"sprint_support_user_info".*?"(nickname)".*?"(nickname)".*?"(nickname)"', '-', re_text)

			try:
				nick_name = re.findall('"nickname":"(.*?)",', re_text)
			except:
				nick_name = ['none']
			try:
				user_id = re.findall('"short_id":"(\d+)"', re_text)
				if user_id[0] == '0':
					user_id = re.findall('"unique_id":"(.*?)",', re_text)
			except:
				user_id = ['none']
			try:
				fans_count = re.findall('"fans_count":(\d+)', re_text)
			except:
				fans_count = ['null', 'null', 'null']
			try:
				total_fav = re.findall('"total_favorited": ?(\d+)', re_text)
			except:
				total_fav = ['null']

			# 	# nick_name取最后一个，避免粉丝的昵称影响
			# 	f.write(nick_name[-1] + '|' + user_id[0] + '|' + total_fav[0] + '|' + fans_count[0] + '|' + fans_count[1] + '|' + fans_count[2] + '\n')
			name_list = re.findall('[\u4e00-\u9fa5\u0020-\u0080]', nick_name[-1])
			nickname = ''
			for letter in name_list:
				nickname += letter
			userid = user_id[0]
			totalfav = int(total_fav[0])
			fansdou = int(fans_count[0])
			fanstou = int(fans_count[1])
			fanshuo = int(fans_count[2])
			# print(nickname + '|' + user_id[0] + '|' + total_fav[0] + '|' + fans_count[0] + '|' + fans_count[1] + '|' + fans_count[2] + '\n')

			crsql = "INSERT INTO user_info(nickname, user_id, total_fav, fans_dou, fans_tou, fans_huo, flg) \
					        VALUES (%s, %s, %s, %s, %s, %s, %s)"

			gxsql = "UPDATE user_info SET nickname=%s, total_fav=%s, fans_dou=%s, fans_tou=%s, fans_huo=%s, flg=1 WHERE user_id = %s"
			try:
				cursor.execute(crsql, (nickname, userid, totalfav, fansdou, fanstou, fanshuo, 1))
				db.commit()
				print(nickname + userid + '详细信息已保存')
			except:
				try:
					cursor.execute(gxsql, (nickname, totalfav, fansdou, fanstou, fanshuo, userid))
					db.commit()
					print(nickname + userid + '详细信息已更新')
				except:

					db.rollback()
		# 判断是否是作品的请求
		if '/aweme/v1/aweme/post/' in flow.request.url:
			# 加上re.S参数，表示.可以匹配包括换行以内的所有字符
			try:
				video = re.findall('"(\d*?)","desc":"(.*?)".*?"video".*?"url_list":\["(.*?)","(.*?)"', re_text, flags=re.S)
			except:
				video = []
				save_error(re_text)
			try:
				name = re.search('"nickname":"(.*?)"', re_text).group(1)
			except:
				name = ''
				save_error(re_text)
			try:
				userid = re.search('"short_id":"(\d+)"', re_text).group(1)
				if userid[0] == '0':
					userid = re.search('"unique_id":"(.*?)",', re_text).group(1)
			except:
				userid = ['none']
			name_list = re.findall('[\u4e00-\u9fa5\u0030-\u0039\u0041-\u005A\u0061-\u007A]', name)
			nickname = ''
			for letter in name_list:
				nickname += letter
			db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
			                     database=dy_setting.database, charset=dy_setting.charset)
			# 使用cursor()方法获取操作游标
			cursor = db.cursor()
			for i in video:
				name_list = re.findall('[\u4e00-\u9fa5\u0030-\u0039\u0041-\u005A\u0061-\u007A]*', i[1])[0]
				videoname = name_list + str(time.time())
				videoid = i[0]
				videolink1 = i[2]
				videolink2 = i[3]
				linktime = time.time()
				videotime = time.strftime("%Y-%m-%d %H:%M:%S")

				crsql = "INSERT INTO video(nickname, user_id, videoname, videolink1, videolink2, linktime, videotime, videoid, flg) \
								        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
				try:
					cursor.execute(crsql,
					               (nickname, userid, videoname, videolink1, videolink2, linktime, videotime, videoid, 0))
					db.commit()
					print(videoname + '   保存成功')
				except:
					print(videoname + '    已存在')
					db.rollback()
	except:
		pass
	db.close()



