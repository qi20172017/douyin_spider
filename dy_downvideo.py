# !/usr/bin/env python
# coding:utf-8
# Time:2019/10/12 15:56
# write_by:QiFuMin
# script_name:downvideo.py
import requests
import MySQLdb
import dy_setting
import time
import os


class Downvideo():

	def get_link(self):
		db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
			                     database=dy_setting.database, charset=dy_setting.charset)
		cursor = db.cursor()
		sql_cx = "SELECT * FROM video WHERE flg = 0 LIMIT 1 "
		cursor.execute(sql_cx)
		results = cursor.fetchall()
		db.close()
		return results

	def download(self, results):
		if results != ():
			username = results[0][0]
			userid = results[0][1]
			videoid = results[0][2]
			videoname = results[0][3]
			videolink1 = results[0][4]
			videolink2 = results[0][5]
			auth_path = 'd:\\douyin_video\\' + username + userid
			try:
				os.makedirs(auth_path)
			except:
				pass
				# print("This folder already exists")
			try:
				res = requests.get(videolink1, headers=dy_setting.headers())
			except:
				try:
					res = requests.get(videolink2, headers=dy_setting.headers())
				except:
					res = 'NONE'
			if res == 'NONE':
				print('链接打开失败')
				print(videolink1)
				print(videolink2)
				file_path = 'NONE'
			else:
				file_path = auth_path + '\\' + videoname + '.mp4'
				with open(file_path, 'wb') as f:
					f.write(res.content)
		else:
			file_path = 'NONE'
			videoid = 'NONE'

		return file_path, videoid

	def update(self, file_path, videoid):
		if file_path == 'NONE' and videoid == 'NONE':
			print('已经全部下载完成')
			time.sleep(3)
		else:
			db = MySQLdb.connect(host=dy_setting.host, port=dy_setting.port, user=dy_setting.user, password=dy_setting.password,
			                     database=dy_setting.database, charset=dy_setting.charset)
			cursor = db.cursor()
			sql_gx = "UPDATE video SET flg=%s,videotime=%s,saveadd=%s WHERE  videoid= %s"
			videotime = time.strftime("%Y-%m-%d %H:%M:%S")
			if file_path == 'NONE':
				# 2 表示下载失败
				flg_code = 2
			else:
				# 1表示正常被下载
				flg_code = 1
			try:
				cursor.execute(sql_gx, (flg_code, videotime, file_path, videoid))
				print(file_path + '下载后更新成功')
				db.commit()
			except:
				print('Updata_Secret_ID_flg:Error')
				db.rollback()
			db.close()

	def start_down(self):
		while True:
			res = self.get_link()
			file_path, videoid = self.download(res)
			self.update(file_path, videoid)


if __name__ == '__main__':
	dv = Downvideo()
	dv.start_down()





