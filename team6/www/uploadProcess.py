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
			return redirect(request.url)

		file = request.files.get('file')
		if file.filename == '':
			return redirect(request.url)

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
			if checkUserExist(username) == False:
				return render_template('upload.html', falseInfo="No such username!")
			else:
				flag = dbInsertImg(filename, username, image_category, author, intro)
				if flag != True:
					return render_template('upload.html', falseInfo=flag)
			#database working not started yet
			#######
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			#return redirect(url_for('uploadProcess.showPage', filename=filename))	# see uploaded img
			#return redirect(url_for('init'))		# back to homepage
			return render_template('upload.html', uploadDone="Uploaded done!")
			
	return render_template('upload.html')
	

@uploadProcess.route('/check/')
def showProcess():
	return redirect(url_for('uploadProcess.showPage', filename=filename))

@uploadProcess.route('/show/<filename>')
def showPage(filename):
	# send image to frond-end
	img_stream = return_img_stream(UPLOAD_FOLDER+'/'+filename)
	return render_template('show.html', img_stream=img_stream)
	
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
		falseinfo = "Exst image name!"
		print(falseinfo)
		db.close()
		return falseinfo
