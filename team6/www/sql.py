import sqlite3
import dbutil
import time

global db
dbname = 'userdb.db'

def dbQuery(choice, table):
	db = dbutil.dbUtils(dbname)
	sql = "select " + choice + " from " + table
	userList = db.db_action(sql, 1)
	db.close()
	return userList
	
def dbInsertUser(userid, username, passwd):
	db = dbutil.dbUtils(dbname)
	if checkUserExist(username):
		return "Exist user!!!"
	user = "(" + userid + ",'" + username + "','" + passwd + "')"
	sql = 'insert into user values ' + user
	if db.db_action(sql, 0) == True:
		print("User insert done.")
	db.close()
	return "insert done."
	
def dbInsertMovie(movieid, movie, tag, score, introduction):
	db = dbutil.dbUtils(dbname)
	movie = "(" + movieid + ",'" + movie + "','" + tag + "'," + score + ",'" + introduction + "')"
	sql = 'insert into movie_info values ' + movie
	if db.db_action(sql, 0) == True:
		print("User insert done.")
	db.close()
	return "insert done."
	
def checkUserExist(username):
	userList = dbQuery("username", "user")
	for i in userList:
		if username == i[0]:
			return True
	return False
	
def checkUserList(table):
	db = dbutil.dbUtils(dbname)
	sql = "select * from " + table
	userList = db.db_action(sql,1)
	for user in userList:
		print(user)
	db.close()
	
def dbUpdate(moviename, moviescore):
	db = dbutil.dbUtils(dbname)
	sql = "select score, numberOfScoring from movie_info where movie_name = '" + moviename + "'"
	scoreL = db.db_action(sql, 1)
	score = float(scoreL[0][0])
	n = float(scoreL[0][1])
	if score == -1 and n == 0:
		score = moviescore
	else:
		score = (moviescore + (score*n)) / (n+1)
	# only keep one decimal point
	score = int(score*10)/10
	n += 1
	
	#UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6
	sql = "update movie_info set score = " + str(score) + ", numberOfScoring = " + str(n) + " where movie_name = '" + moviename + "'"
	flag = db.db_action(sql, 0)
	db.close()
	
def dbDelete(db, table):
	# DROP TABLE table_name
	db = dbutil.dbUtils(dbname)
	sql = "drop table %s" % (table)	
	if db.db_action(sql, 0) == True:
		print("%s delete done." % (table))
	db.close()
	
def dbInsertImg(imgname, uploader, categroy, author, intro, tag='null'):
	db = dbutil.dbUtils(dbname)
	# sql = "I love %s" % ('piano') | 'insert into img values '+ imgInfo
	sql = "insert into img values (null, '%s', '%s', '%s', '%s', '%s', '%s', 0)" % (imgname, uploader, categroy, author, intro, tag)
	#if db.db_action(sql, 0) == True:
	#	print("User insert done.")
	try:
		db.db_action(sql, 0)
		print("Img insert done.")
	except:
		print("Exst img name!")
	db.close()
	
def fetchImgInfo(filename):
	imgList = dbQuery("*", "img")
	for i in imgList:
		if filename == i[1]:
			return list(i)
	return False
	
def addDbColumn(table, column, columnAttri):
	db = dbutil.dbUtils(dbname)
	sql = "alter table %s add column %s %s" % (table, column, columnAttri)
	try:
		db.db_action(sql, 0)
		print("Column insert done.")
	except:
		print("Exst column!")
	db.close()

def dbInsertReview(imgid, userid, username, content):
	db = dbutil.dbUtils(dbname)
	created_at = time.time()
	sql = "insert into reviews values (null, '%s', '%s', '%s', '%s', '%f')" % (imgid, userid, username, content, created_at)
	try:
		db.db_action(sql, 0)
		print("Review insert done.")
	except:
		print("Failed")
	db.close()
	
def dbTableDelete(table, condition):
	db = dbutil.dbUtils(dbname)
	sql = "delete from %s %s;" % (table, condition)
	print(sql)
	#sql = "PRAGMA  table_info(img)"
	db.db_action(sql, 0)
	for i in l:
		print(i)
	"""try:
		db.db_action(sql, 0)
		print("Delete done.")
	except:
		print("Failed")"""
	db.close()

def dbImgSelect(condition=''):
	db = dbutil.dbUtils(dbname)
	sql = "select imgname from img %s" % (condition)
	imgList = db.db_action(sql, 1)
	db.close()
	return imgList

if __name__ == "__main__":
	#print(dbInsertUser('null', 'eee', '1234'))
	#dbInsertMovie('null', 'movie2', 'comedy', '-1132.12', 'text')
	#dbUpdate("movie1", 0)
	#ALTER TABLE OLD_COMPANY ADD COLUMN SEX char(1);
	#dbInsertReview('10', '5', 'test', 'My favorite work.')
	#dbTableDelete("img", 'where imgname="Lighty.png"')
	
	
	tlist = dbQuery("*", "img")
	#tlist = dbImgSelect("where author = 'TZ'")
	for i in tlist:
		print(i)
	print('***')
	
	#dbInsertImg('di.png', 'imgtest', '0', 'TZ', '')
	#print(fetchImgInfo('ia.png'))
	#dbDelete('demo', 'img')
	#addDbColumn('img', 'expectedPrice', 'integer')
