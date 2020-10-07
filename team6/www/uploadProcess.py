from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory
import os
from werkzeug.utils import secure_filename
import base64

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
			filename = secure_filename(file.filename)
			# change original filename to input name
			if input_name != "":
				filename = input_name + '.' + filename.rsplit('.', 1)[1].lower()
			
			#######	
			#database working not started yet
			#######
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			return redirect(url_for('uploadProcess.show', filename=filename))
			
	return render_template('upload.html')

@uploadProcess.route('/show/<filename>')
def show(filename):
	# send image to frond-end
	img_stream = return_img_stream(UPLOAD_FOLDER+'/'+filename)
	return render_template('show.html', img_stream=img_stream)
