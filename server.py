from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5
import re

app = Flask(__name__)
mysql = MySQLConnector(app,'reddit')
app.secret_key = "ThisIsSecret!"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

@app.route('/')
def index():
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    return render_template('index.html', all_users=users)

@app.route('/create', methods=['POST'])
def create_user():
    username = request.form['username'] #username= login username 
    password = request.form['password']
#if username ---   
    if len(request.form['username']) < 2:  
        flash('Username name cannot be blank!')
        return redirect('/')
    elif not NAME_REGEX.match(username): # if invalid format
        flash('Invalid format')
        return redirect('/')
#password---
    if len(request.form['password']) < 8: #less than 2 letters 
        flash('password needs to be more than 8!')
        return redirect('/')
    if (request.form['password']) != request.form['confirmpassword']:
        flash('password is not matched!')
    else: 
        password = md5.new(request.form['password']).hexdigest()
        insert_query = "INSERT INTO users (username, password) VALUES (:username, :password )"
        query_data = { 'username': username, 'password': password }
        mysql.query_db(insert_query, query_data)
        flash ('Thanks!')
    return redirect('/')
    




@app.route('/login', methods=['post'])
def longinprocess():
	# username = request.form['username']

    hash_pass = md5.new(request.form['password']).hexdigest()
    print "password: ", hash_pass
    # query1 = "SELECT username, password FROM users WHERE username = :username AND password = :password"
    # data1 = { "username": request.form['username'], "password": hash_pass}
    query2 = "SELECT * FROM users where users.username = :username"
    data2 = { 'users.username': username }  
    #user = mysql.query_db(user_query, query_data)
    user = mysql.query_db(query2, data2)

    # show_query = mysql.query_db(query1, data1)
    # users = mysql.query_db(query2, data2)

    # user_query = "SELECT * FROM users where users.username = :username"
	# query_data = { 'username': username}
    # user = mysql.query_db(user_query, query_data)
    # print "show_query: ", show_query ------how to print out 
   
    if show_query ==[]:
        flash('Wrong login information')
        return redirect('/')      
    else:
        session['hold']= users.id[0]['id'] #holdsession
        return redirect('/welcome')
 
@app.route('/post', methods =['POST'])
def post_message():
    if 'hold' in session:
        name_query = 'SELECT * FROM users WHERE id = :id'
        id_data = { 'id': session['hold'] }
        id_user = mysql.query_db(name_query,id_data)
        username = id_user[0]['username']

        query_post = 'SELECT posts.id, text, posts.created_at, posts.updated_at, users.id as author_id, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY created_at DESC'
        query_comment = 'SELECT comments.id, posts_id, comment,comments.created_at,users.id as author_id,users.username FROM comments JOIN users ON comments.user_id = users.id'
        posts = mysql.query_db(query_post)
        comments = mysql.query_db(query_comment)
        return render_template('post.html', username = username, posts = posts, comments = comments)
    else:
        return redirect('/post')
@app.route('/posts_post', methods =['POST'])
def post_post():
    post = request.form['post']
    insert_query_post = "INSERT INTO posts (text, created_at, updated_at, user_id) VALUES(:text,NOW(),NOW(), :user_id)"
    query_data = {
        'post': request.form['post'],
        'user_id' : session['hold']
    }
    mysql.query_db(insert_query_post,query_data)

    return redirect('/post')

@app.route('/post_comment', methods = ['POST'])
def post_comment():
    comment = request.form['comment']
    insert_query_comment = 'INSERT INTO comments (text, created_at, updated_at, user_id, post_id) VALUES (:text, NOW(), NOW(), :user_id, :post_id)'
    query_data = {
    "text": request.form['text']
    "user_id": session['hold']
    "post_id": request.form['post_id']
    }
    mysql.query_db(insert_query_comment,query_data)

    return redirect('/post')



# @app.route('/add_subred', methods=['post'])
# def add_subred():
#         subreddit = request.form['subreddit']
#         insert_query_add_sub= "INSERT INTO subreddits (user_id, subreddit_id) VALUES (:user_id, :subreddit_id,)"
#         query_data = {
#             "subreddit": request.form['subreddit'],
#             "users_id": session['id']
#         }
#         mysql.query_db(insert_query_comment, query_data)
#             return render_template('add_sub.html')


#@app.route('')
app.run(debug=True)