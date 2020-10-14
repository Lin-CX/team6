from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory
import os
from werkzeug.utils import secure_filename
import base64
import dbutil
import sqlite3

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
			username = session['username']
			filename = secure_filename(file.filename)
			# change original filename to input name
			if input_name != "":
				filename = input_name + '.' + filename.rsplit('.', 1)[1].lower()
			
			#######
			# database operating
			if checkUserExist(username) == False:
				return render_template('upload.html', falseInfo="No such username!")
			else:
				flag = dbInsertImg(filename, username, image_category, author, intro)
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
			pass
		# search by uploader
		else:
			pass

	return render_template("searchimg.html")

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
		imgList[1] = imgList[1].rsplit('.', 1)[0]			# remove the filename extension
		return render_template('showimg.html', img_stream=img_stream, imgInfo=imgList)
	
@uploadProcess.route('/likeprocess', methods=['POST'])
def likeprocess():
	#filename = 'dia.png'		# temp
	filename = request.form["filename"]
	filename_extension = request.form["filename_extension"]
	fullfilename = filename+'.'+filename_extension
	likeOrDislike = request.form["likeOrDislike"]
	likeDbProcess(fullfilename, int(likeOrDislike))
	return redirect(url_for('uploadProcess.showPage', filename=fullfilename))
	
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
	
def dbInsertImg(imgname, uploader, categroy='unknow', author='unknow', intro='', tag=''):
	db = dbutil.dbUtils('userdb.db')
	sql = "insert into img values (null, '%s', '%s', '%s', '%s', '%s', '%s', 0)" % (imgname, uploader, categroy, author, intro, tag)
	try:
		db.db_action(sql, 0)
		db.close()
		return True
	except:
		falseinfo = "Exist image name!"
		print(falseinfo)
		db.close()
		return falseinfo
