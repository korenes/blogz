from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title_name = request.form['entryfortitle']
        post_name = request.form['writingarea']
        new_blog = Blog(title_name, post_name)
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

        return render_template("blog.html", blogs=blogs)


if __name__ == '__main__':
    app.run()