from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5

app = Flask(__name__)
mysql = MySQLConnector(app,'reddit')

@app.route('/')
def index():
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    return render_template('index.html', all_users=users)

@app.route('/create', methods=['POST'])
def create_user():
    username = request.form['username']
    password = md5.new(request.form['password']).hexdigest()
    #passwordconfirm = md5.new(request.form ['password'].hexdigest())
    insert_query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (:username, :password, NOW(), NOW())"
    query_data = { 'username': username, 'password': password }
    mysql.query_db(insert_query, query_data)
    return redirect('/create')
#@app.route('/reset', methods = ['POST'])
#def reset():

@app.route('/login', methods=['post'])
def longinprocess():
	username = request.form['username']
	password = md5.new(request.form['password']).hexdigest()
	user_query = "SELECT * FROM users where users.username = :username"
	query_data = { 'username': username}
	user = mysql.query_db(user_query, query_data)

	print user #changed from users to user/ Line 32
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	# invalid username
	if len(request.form['username'])<1:
		flash("Valid Email format!")
		return redirect('/login')
	# user doesn't exists
	elif len(request.form['password']) <1:
		flash("no password")
		return redirect('/login')
	# invalid user
	elif  not user: #this was user to begin with????
		flash("Wrong email")
		return redirect('/login')
	# invalid password
	elif user[0]['password'] != password:
		flash("Wrong password")
		return redirect('/login') #redirect('/login_page')
	# correct info
	else:
		session['id'] = user[0]['id']
		return redirect ('/welcome')



#@app.route('')
app.run(debug=True)