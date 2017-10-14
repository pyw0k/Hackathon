from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'reddit')
@app.route('/')
def index():
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    return render_template('index.html', all_users=users)
@app.route('/usersreg', methods=['POST'])
def create():
	query = "INSERT INTO users(username, password, created_at,updated_at) VALUES(:users, :password, NOW(),NOW())"
  # data=  {
    #         'username': request.form['username'],
             #'password':  request.form['password']
       #    }
	mysql.query_db(query, data)
	return redirect('/')
app.run(debug=True)