# ------------------------------------------
#  Author: 임준상
#          Computer Science & Engineering
#          College of Informatics, Korea Univ.
#
#  Date:   Oct 16, 2020
#
#  Function: Image upload, Showing, Searching, management, Like
# ------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory
import os
from werkzeug.utils import secure_filename
import base64
import dbutil
import sqlite3
import time
import random

uploadProcess = Blueprint('uploadProcess', __name__)

UPLOAD_FOLDER = 'static/upload_file'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# check the file format
def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

# receive file and add file info to database
@uploadProcess.route("/upload", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if "file" not in request.files:
			return render_template('upload.html', falseInfo="Please select file!")

		file = request.files.get('file')
		if file.filename == '':
			return render_template('upload.html', falseInfo="Please select file!")

		if file and allowed_file(file.filename):
			# 1: 회화; 2: 서양화; 3: 동양화
			image_category = request.form["category"]
			input_name = request.form["imagename"]
			intro = request.form["intro"]
			author = request.form["author"]
			ep = request.form["expectedprice"]
			username = session['username']
			filename = secure_filename(file.filename)
			# change original filename to input name
			if input_name != "":
				filename = input_name + '.' + filename.rsplit('.', 1)[-1].lower()
			
			#######
			# database operating
			if checkUserExist(username) == False:
				return render_template('upload.html', falseInfo="No such username!")
			else:
				if author == '':
					author = session['username']
<<<<<<< HEAD
				flag = dbInsertImg(filename, username, image_category, author, intro, expectedprice=ep)
=======
				flag = dbInsertImg(filename, username, image_category, author, intro)
>>>>>>> 1ba4d0e2fb3e6c59341975d7002968423d6db003
				if flag != True:
					return render_template('upload.html', falseInfo=flag)
			#######
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			#return redirect(url_for('uploadProcess.showPage', filename=filename))	# see uploaded img
			#return redirect(url_for('init'))		# back to homepage
			return render_template('upload.html', uploadDone="Uploaded done!")
			
	return render_template('upload.html')
	
def checkFilename(filename):
	namelist = dbQuery("imgname", "img")
	for i in namelist:
			if filename == i[0].rsplit('.', 1)[0]:
				filename = i[0]
				return filename
	return False
	
@uploadProcess.route('/searchimg', methods=['GET', 'POST'])
def searchimg():
	if request.method == "POST":
		searchby = request.form["searchby"]
		searchinfo = request.form["searchinfo"]
		
		# search by imagename
		if searchby == '1':
			if searchinfo == "":
				return render_template("searchimg.html", falseInfo="Empty filename!")
			return redirect(url_for("uploadProcess.showProcess", filename=searchinfo))
		
		# search by author		
		elif searchby == '2':
			if searchinfo == "":
				return render_template("searchimg.html", falseInfo="Empty serchInfo!")
			temp = "where author = '%s'" % (searchinfo)
			#temp = "where uploader = '%s'" % ('admin')
			imgList = dbImgSelect(temp)
			img_streamList = []
			for filename in imgList:
				temp = []
				temp.append(return_img_stream(UPLOAD_FOLDER+'/'+filename[0]))
				temp.append(filename[0])
				s = filename[0].rsplit('.', 1)[0]
				temp.append(s)
				img_streamList.append(temp)			#img_streamList[][0]: image stream, img_streamList[][1]: image name(with filename extension), img_streamList[][0]: image name(normal)
			return render_template("img_exhibit.html", img_streamList=img_streamList)
			
		#
		else:
			pass

	return render_template("searchimg.html")
	
@uploadProcess.route('/lookaround')
def lookaround():
	imgList = dbImgSelect()
	length = len(imgList)
	
	l = []
	for i in range(length):
		l.append(i)
	random.shuffle(l)
	if length > 6:
		l = l[:6]
	
	img_streamList = []
	for i in l:
		temp = []
		filename = imgList[i][0]
		temp.append(return_img_stream(UPLOAD_FOLDER+'/'+filename))
		temp.append(filename)
		s = filename.rsplit('.', 1)[0]
		temp.append(s)
		img_streamList.append(temp)
		
	return render_template("img_exhibit.html", img_streamList=img_streamList)

@uploadProcess.route('/showProcess')
def showProcess():
	filename = request.args.get('filename')	
	if filename == "":
		return render_template("searchimg.html", falseInfo="Empty filename!")
	checkinfo = checkFilename(filename)	# if exist, return full filename; if not, return False
	if checkinfo == False:
		return render_template('searchimg.html', falseInfo="No this image!")
	else:			
		return redirect(url_for('uploadProcess.showPage', filename=checkinfo))

@uploadProcess.route('/showPage')
def showPage():
	filename = request.args.get('filename')
	# send image to frond-end
	imgList = fetchImgInfo(filename)
	if imgList == False:
		return render_template('searchimg.html', falseInfo="No this image!")
	else:
		img_stream = return_img_stream(UPLOAD_FOLDER+'/'+filename)
		imgList.append(imgList[1].rsplit('.', 1)[1])
		imgList[1] = imgList[1].rsplit('.', 1)[0]			# remove filename extension
		return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList)
	
@uploadProcess.route('/likeprocess', methods=['POST'])
def likeprocess():
	#filename = 'dia.png'		# temp
	filename = request.form["filename"]
	filename_extension = request.form["filename_extension"]
	like_type = request.form["like_type"]
	fullfilename = filename+'.'+filename_extension
	filename = fullfilename
	likeOrDislike = request.form["likeOrDislike"]
	likeDbProcess(fullfilename, int(likeOrDislike))
	#return redirect(url_for('uploadProcess.showPage', filename=fullfilename))
	imgList = fetchImgInfo(filename)
	img_stream = return_img_stream(UPLOAD_FOLDER+'/'+filename)
	imgList.append(imgList[1].rsplit('.', 1)[1])
	imgList[1] = imgList[1].rsplit('.', 1)[0]			# remove filename extension
	if like_type == '2':
		if likeOrDislike == '1':
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=0)	# like
		else:
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=1)	# dislike
	elif like_type == '1':
		if likeOrDislike == '2':
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=0)	# like
		else:
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=2)	# normal
	else:
		if likeOrDislike == '-1':
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=2)	# normal
		else:
			return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList, isLiked=1)	# dislike
	
@uploadProcess.route('/checkImgDetails')
def checkImgDetails():
	filename = request.args.get('filename')
	fullfilename = checkFilename(filename)
	return send_from_directory(UPLOAD_FOLDER, fullfilename, as_attachment=False)
	
###############################################################
	
@uploadProcess.route('/imgManagementPage', methods=['POST', 'GET'])
def imgManagementPage():
	if request.method == "POST":
		filename = request.form["filename"]
		print(filename)
		return redirect(url_for('uploadProcess.showProcess', filename=filename))
	
	temp = "where uploader = '%s'" % (session['username'])
	#temp = "where uploader = '%s'" % ('admin')
	imgList = dbImgSelect(temp)
	#length = len(imgList)
	
	img_streamList = []
	for filename in imgList:
		temp = []
		temp.append(return_img_stream(UPLOAD_FOLDER+'/'+filename[0]))
		temp.append(filename[0])
		s = filename[0].rsplit('.', 1)[0]
		temp.append(s)
		img_streamList.append(temp)
	#img_streamList[][0]: image stream, img_streamList[][1]: image name(with filename extension)
	return render_template("manaPage.html", img_streamList=img_streamList)
	
@uploadProcess.route('/imgDelete', methods=['POST'])
def imgDelete():
	imgname = request.form["imgname"]
	fullfilename = checkFilename(imgname)
	condition = 'where imgname="%s"' % (fullfilename)
	dbTableDelete('img', condition)
	#print(condition)
	
	return redirect(url_for("uploadProcess.imgManagementPage"))

def dbTableDelete(table, condition=''):
	db = dbutil.dbUtils('userdb.db')
	sql = "delete from %s %s;" % (table, condition)
	try:
		db.db_action(sql, 0)
		print("Delete done.")
	except:
		print("Failed")
	db.close()

def dbImgSelect(condition=''):
	db = dbutil.dbUtils("userdb.db")
	sql = "select imgname from img %s" % (condition)
	imgList = db.db_action(sql, 1)
	db.close()
	return imgList
	
###############################################################	
	
def likeDbProcess(filename, n):
	db = dbutil.dbUtils('userdb.db')
	sql = "select liken from img where imgname = '%s'" % (filename)
	likeL = db.db_action(sql, 1)
	like = likeL[0][0]
	like += n
	sql = "update img set liken = %d where imgname = '%s'" % (like, filename)
	flag = db.db_action(sql, 0)
	db.close()
	return flag
	
def fetchImgInfo(filename):
	imgList = dbQuery("*", "img")
	for i in imgList:
		if filename == i[1]:
			return list(i)
	return False
	
def dbQuery(choice, table):
	db = dbutil.dbUtils('userdb.db')
	sql = "select " + choice + " from " + table
	userList = db.db_action(sql, 1)
	db.close()
	return userList

def checkUserExist(username):
	userList = dbQuery("username", "user")
	for i in userList:
		if username == i[0]:
			return True
	return False
	
def dbInsertImg(imgname, uploader, categroy='unknow', author='unknow', intro='', tag='', expectedprice='0'):
	db = dbutil.dbUtils('userdb.db')
<<<<<<< HEAD
	sql = 'insert into img values (null, "%s", "%s", "%s", "%s", "%s", "%s", 0, %s)' % (imgname, uploader, categroy, author, intro, tag, expectedprice)
	#print("dbinsertImg: %s" % imgname)
	#print(sql)
=======
	sql = 'insert into img values (null, "%s", "%s", "%s", "%s", "%s", "%s", 0)' % (imgname, uploader, categroy, author, intro, tag)
	print("dbinsertImg: %s" % imgname)
>>>>>>> 1ba4d0e2fb3e6c59341975d7002968423d6db003
	try:
		db.db_action(sql, 0)
		db.close()
		return True
	except:
		falseinfo = "Exist image name!"
		print(falseinfo)
		db.close()
		return falseinfo
