# ------------------------------------------
#  Author: 임준상
#          Computer Science & Engineering
#          College of Informatics, Korea Univ.
#
#  Date:   Oct 16, 2020
# ------------------------------------------


from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_from_directory, current_app
import os
from werkzeug.utils import secure_filename
from userProcess import userProcess
from mateProcess import mateProcess
from uploadProcess import uploadProcess

import dbutil

import sqlite3

app =Flask(__name__)
app.secret_key='dlawnstkd'

urls = [userProcess, mateProcess, uploadProcess]
for url in urls:
	app.register_blueprint(url)

@app.route('/operation_guide')
def operation_guide():
	return render_template("operation_guide.html")

@app.route('/')
def init():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, port=1234)
