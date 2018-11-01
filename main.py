from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y234ukt&PP3S'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref= 'owner' )

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(username = session['username']).first()
    if request.method == 'POST':

        title_name = request.form['entryfortitle']
        post_name = request.form['writingarea']
        new_blog = Blog(title_name, post_name, owner)
        title_error = ''
        writingarea_error = ''
        if title_name == '':
            title_error = "Please enter a title"

        if post_name == '':
            writingarea_error = "Please enter a blog"
            return render_template("newpost.html", title_error=title_error, writingarea_error=writingarea_error )
        else:
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id={0}".format(new_blog.id))


    return render_template("newpost.html")


@app.route('/blog', methods=['GET'])
def blog():
    blogpost=request.args.get('id')
    if blogpost is not None:
        blogs = Blog.query.filter_by(id=blogpost)
        return render_template("blogpage.html", blogs=blogs)

    else:
        blogs = Blog.query.all()
        username = request.args.get('user')

        if username:
            user = User.query.filter_by(username=username).first()
            blogs = Blog.query.filter_by(owner_id = user.id)

        return render_template("blog.html", blogs=blogs)

@app.route('/', methods=['POST','GET'])
def index():
    users= User.query.all()
    return render_template("index.html", users=users)



@app.before_request
def require_login():
    allowed_routes = ['login','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == '' or password == '' or verify == '':
            flash('Please complete all fields, fields cannot be left blank.')
        if password != verify:
            flash('Passwords do not match!')
        if (len(username) <3) or (len(password) <3):
            flash('Username or Password invalid, please enter more than 3 characters!')

    
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            
            flash('Username already exists')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()