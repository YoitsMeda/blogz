from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:poop123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "#decoderring"

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = "db.relationship('Blog', backref='user')"

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    user = db.Column(db.String(120), db.ForeignKey(User.username))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user



@app.route("/", methods=["GET", "POST"])
def index():
    blogs = Blog.query.all()
    return render_template('userpage.html',blogs=blogs)

@app.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    return render_template('bloggers.html', users=users)

@app.route("/profile", methods=["GET"])
def profile():
    user = request.args.get("user")
    blogs = Blog.query.filter_by(user=user).all()
    return render_template("userpage.html",blogs=blogs)

@app.route("/display", methods=["GET"])
def display():
    id = request.args.get("id")
    blog = Blog.query.filter_by(id=id).first()
    return render_template("page.html", title=blog.title, user=blog.user, blog=blog.body)

@app.route("/add", methods=["GET", "POST"])
def add_blog():
    if request.method =="POST":
        title = (request.form["Title"])
        body = (request.form["Body"])
        if len((title.strip())) == 0:
            flash("Error: You forgot your title")
        if len((body.strip())) == 0:
            return render_template("add.html")
        new_blog = Blog(title,body,session["username"])
        db.session.add(new_blog)
        db.session.commit()
        return redirect("/display?id={}".format(new_blog.id))
    else:
        return render_template("add.html")

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'users', 'profile', 'display', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return render_template("login.html")

@app.route('/login', methods=["GET","POST"])
def login():
    print("login")
    if request.method =="POST":
        username = (request.form["username"]).lower()
        password = request.form["pass1"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Hey you did it login complete")
            return redirect("/add")
        elif username and user.password != password:
            flash("That's a baddd Password My Dude! Try Again!")
            return redirect("/login")
        else:
            flash("Oh no! Somethings is wrong My Dude")
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')

@app.route("/signup")
def signup():
    print("SIGN UP")
    return render_template("signup.html")

@app.route("/register", methods=['GET','POST'])
def register():
    username = request.form['username']
    print(1)
    password = request.form['password']
    print(2)
    verifypassword = request.form['verifypassword']
    print(3)
    email = request.form['email']
    print(username,password)

# def existing_user():
#     existing_user = User.query.filter_by(username=username).first()
#
#     # if " " in username:
#     #     flash("No spaces allowed Try again.","error")
#     # if len(username) < 3 or len(username) > 25:
#     #     flash("I think well how do you I tell you this....It might be too long or too short for my liking.....That's what she said!","error")
#     # if " " in password:
#     #     flash("Hey NO spaces geez...You just think you're special because you're a person and add spaces anywhere..WELL NO. Try Again!")
#     # if len(password) < 3 or len(password) > 25:
#     #     flash("I think well how do you I tell you this....It might be too long or too short for my liking.....That's what she said! Try A New Password Please!","error")
#     # if password != verifypassword:
#     #     flash("You just typed it in and you forgot...oh boy we are doomed. Please re-verify your password.","error")
#     # email_error = ""
#     # if " " in email:
#     #     flash("Hey NO spaces geez...You just think you're special because you're a person and add spaces anywhere..WELL NO. Try Again!","error")
#     # if "@" not in email:
#     #     flash("Riddle me this...I am what every email has and you forgot me what am I?.................Give up? You forgot your @. Try Again Please.", error)
#     # errorcount = email.count('@')
#     # if errorcount > 1:
#     #     flash("Email Error Try Again",error)
#     # if "." not in email:
#     #     flash("Email Error Try Again",error)
#
#     if existing_user in register:
#         flash("Please login")
#         return render_template("login.html")
#         # if not username_error and not pass_error and not email_error:
#         #     return render_template("login.html", username=username)
#     #if len(email) > 0 and (len(email) < 3 or len(email) > 20):
#         #email_error = "It either too long or too short....Try again."
#     return render_template("signup.html")
    # if len(username_error)== 0 and len(pass_error)== 0 and len(email_error)== 0:
    #     return render_template("welcome.html", username=username)
    # else: Checks for no errors, redirecting to a Welcome page instead.  Else goes back to form.

    # if len(username_error)== 0 and len(pass_error)== 0 and len(email_error)== 0:
    new_user = User(username,password)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = new_user.username
    flash("Good Job!! There is hope you know how to fill out a form! Don't worry I won't tell anyone that Google helped you.")
    return render_template("userpage.html", username=username)

    return render_template("signup.html",
        username=username,
        username_error=username_error,
        pass_error=pass_error,
        email=email, email_error=email_error)


if __name__ == "__main__":
    app.run()
