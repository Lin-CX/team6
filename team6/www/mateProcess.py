from flask import Blueprint, render_template, session, url_for, request, redirect

import dbutil
import sqlite3

mateProcess = Blueprint('mateProcess', __name__)

def dbQuery(choice, table):
	db = dbutil.dbUtils('userdb.db')
	sql = "select " + choice + " from " + table
	movieList = db.db_action(sql, 1)
	db.close()
	return movieList

def dbUpdate(moviename, moviescore):
	db = dbutil.dbUtils('userdb.db')
	sql = "select score, numberOfScoring from movie_info where movie_name = '" + moviename + "'"
	scoreL = db.db_action(sql, 1)
	score = float(scoreL[0][0])
	n = float(scoreL[0][1])
	if score == -1 and n == 0:
		score = moviescore
	else:
		score = (moviescore + (score*n)) / (n+1)
	# only keep one decimal point
	score = int(score*100000)/100000
	n += 1
	#syntax: UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6
	sql = "update movie_info set score = " + str(score) + ", numberOfScoring = " + str(n) + " where movie_name = '" + moviename + "'"
	flag = db.db_action(sql, 0)
	db.close()
	
	return flag

def fetchMovie(moviename):
	movieList = dbQuery("*", "movie_info")
	for i in movieList:
		if moviename == i[1]:
			return list(i)
	return False

@mateProcess.route('/movie', methods=["POST", "GET"])
def moviePage():
	if request.method == "POST":
		moviename = request.form["moviename"]
		global movieObject
		movieObject = moviename
		fetchInfo = fetchMovie(moviename)
		if fetchInfo != False:
			return render_template("moviePage.html", searchPage=0, movieSearInfo=fetchInfo)
		else:
			return render_template("moviePage.html", searchPage=1, falseInfo="No this movie!", movieSearInfo=fetchInfo)
		
	return render_template("moviePage.html", searchPage=1)
	
@mateProcess.route('/scoring', methods=["POST"])
def movieScoringDone():
	movieScore = request.form["score"]
	global movieObject
	dbUpdate(movieObject, int(movieScore))
	return render_template("moviePage.html", searchPage=1)

