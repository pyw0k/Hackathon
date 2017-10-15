from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

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


#@app.route('')
app.run(debug=True)