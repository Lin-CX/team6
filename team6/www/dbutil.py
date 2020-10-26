# ------------------------------------------
#  Author:	Peter Cao
#			https://zhuanlan.zhihu.com/p/91075748
#
#  Date:	Oct 16, 2020
# ------------------------------------------

class dbUtils:
	def __init__(self, dbName):	# connect to database
		import sqlite3
		self.conn = sqlite3.connect(dbName)

	def db_action(self, sql, actionType=0):
		try:
			res = self.conn.execute(sql)
			if actionType == 1:	# query operation
				return res.fetchall()
			else:				# insert, delete or update operation
				return True
		except ValueError as e:
			print(e)

	def close(self):			# close database
		self.conn.commit()
		self.conn.close()

