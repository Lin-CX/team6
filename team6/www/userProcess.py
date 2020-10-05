from flask import Blueprint, render_template, session, url_for, request, redirect

import dbutil
import sqlite3

userProcess = Blueprint('userProcess', __name__)

@userProcess.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == "POST":
		username = request.form["username"]
		email = request.form["email"]
		passwd = request.form["passwd"]
		return redirect(url_for("userProcess.registerProcess",
								username=username,
								email=email,
								passwd=passwd))
	return render_template('register.html')
	
@userProcess.route('/registerProcess', methods=['GET'])
def registerProcess():	
	username = request.args.get('username')
	email = request.args.get('email')
	passwd = request.args.get('passwd')
	insertInfo = dbInsertUser('null', username, passwd)
	if insertInfo == True:
		session['username'] = username
		return redirect(url_for('init'))
	else:
		session['username'] = ''
		return render_template('register.html', falseInfo=insertInfo)
		
def dbQuery(choice, table):
	db = dbutil.dbUtils('userdb.db')
	sql = "select " + choice + " from " + table
	userList = db.db_action(sql, 1)
	db.close()
	return userList
	
# if exist, return true
def checkUserExist(username):
	userList = dbQuery("username", "user")
	for i in userList:
		if username == i[0]:
			return True
	return False
	
# if matched, return true
def checkSignin(username, passwd):
	userList = dbQuery("username, userpwd", "user")
	if (username, passwd) in userList:
		return True
	else:
		return False

def dbInsertUser(userid, username, passwd):
	db = dbutil.dbUtils('userdb.db')
	userList = dbQuery("username", "user")
	# check exist user
	if checkUserExist(username):
		return "Exist user!!!"
	# insert
	user = "(" + userid + ",'" + username + "','" + passwd + "')"
	sql = 'insert into user values ' + user
	if db.db_action(sql, 0) == True:
		print("User insert done.")
		db.close()
		return True
	else:
		db.close()
		return False
		
@userProcess.route('/signout')
def signoutProcess():
	session.pop('username',None)
	return redirect(url_for('init'))
	
@userProcess.route('/signin')
def signinPage():
	return render_template("signin.html")
	
@userProcess.route('/signinProcess', methods=['POST', 'GET'])
def signinProcessPage():
	if request.method == 'POST':
		username = request.form['un']
		passwd = request.form['passwd']
		if checkSignin(username, passwd):
			session['username'] = username
			return redirect(url_for('init'))
		else:
			return render_template('signin.html', falseInfo="Username or password unmatched!")

	return render_template('signin.html')
