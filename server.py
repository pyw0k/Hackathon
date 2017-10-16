from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5
import re

app = Flask(__name__)
mysql = MySQLConnector(app,'reddit')
app.secret_key = "ThisIsSecret!"
USERNAME_REGEX= re.compile(r'[a-zA-Z0-9.+_-]')

@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session and 'username' in session:
        return redirect('/user')
# -- subreddit posts --
    subpost_query="SELECT posts.text, posts.created_at, users.username, subreddits.url FROM posts JOIN users ON posts.user_id=users.id JOIN subreddits ON posts.subreddit_id=subreddit_id LIMIT 0,50"
    subposts=mysql.query_db(subpost_query)

    return render_template('index.html', all_subposts=subposts)


@app.route('/create', methods=['POST'])
def create_user():
    if len(request.form['username'])<1:
        flash(u"Username cannot be blank!","registration")
    if len(request.form['password'])<8:
        flash(u"Password must be at least 8 characters long","registration")
    if request.form['confirm_password']==request.form['password']:
        flash(u"Password does not match","registration")
    if not USERNAME_REGEX.match(request.form['username']):
        flash(u"Username can only contain alphanumerical and/or.+-_ characters","registration")
    else:
        username= request.form['username']
        password= md5.new(request.form['password']).hexdigest()
        insert_query="INSERT INTO users (username,password) VALUES (:username, :password)"
        query_data={'username':username, 'password':password}
        mysql.query_db(insert_query,query_data)
        return redirect('/user')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    username=request.form['username']
    password = md5.new(request.form['password']).hexdigest()
    user_query= "SELECT * FROM users WHERE users.username= :username AND users.password=:password"
    query_data={'username':username, 'password':password}
    user= mysql.query_db(user_query,query_data)
    if user:
        session['user_id']=int(user[0]['id'])
        session['username']=int(user[0]['id'])
        return redirect('/user')
    else:
        flash(u"User email or password invalid","login")
    return redirect('/')


@app.route('/post', methods =['POST'])
def post_message():
    if 'hold' in session:
        name_query = 'SELECT * FROM users WHERE id = :id'
        id_data = { 'id': session['hold'] }
        id_user = mysql.query_db(name_query,id_data)
        username = id_user[0]['firstname']

        query_post = 'SELECT posts.id, text, posts.created_at, posts.updated_at, users.id as author_id, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY created_at DESC'
        query_comment = 'SELECT comments.id, posts_id, comment,comments.created_at,users.id as author_id,users.username FROM comments JOIN users ON comments.user_id = users.id'
        posts = mysql.query_db(query_post)
        comments = mysql.query_db(query_comment)
        return render_template('post.html', id = users.id, posts = posts, comments = comments)
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

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('username', None)
    return redirect('/')

@app.route('/user')
def userdash():
    subpost_query="SELECT posts.text, posts.created_at, users.username, subreddits.url FROM posts JOIN users ON posts.user_id=users.id JOIN subreddits ON posts.subreddit_id=subreddit_id LIMIT 0,50"
    subposts=mysql.query_db(subpost_query)
    return render_template('user.html', all_subposts=subposts)
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