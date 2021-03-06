from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

# create a flask instance
app = Flask(__name__)

# add database
# SQLite db

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# mySQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xxx@localhost/our_users'

# creating secret key HIDE
app.config['SECRET_KEY'] = "****"

# initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create blog post model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default = datetime.utcnow)
	slug = db.Column(db.String(255))

# create a post form
class PostForm(FlaskForm):
	title = StringField("title", validators = [DataRequired()])
	content = StringField("content", validators = [DataRequired()], widget = TextArea())
	author = StringField("author", validators = [DataRequired()]) 
	slug = StringField("slugfield", validators = [DataRequired()])
	submit = SubmitField("submit", validators = [DataRequired()])


@app.route('/posts')
def posts():
	# grab all the database posts
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# update database
		db.session.add(post)
		db.session.commit()
		flash("post updated")
		return redirect(url_for('post', id=post.id))
	form.title.data = post.title
	form.author.data = post.author
	form.slug.data = post.slug
	form.content.data = post.content
	return render_template('edit_post.html', form=form)


# add post page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Posts(title = form.title.data, content = form.content.data, author = form.author.data, slug = form.slug.data)
		# clear the form
		form.title.data = ''
		form.content.data = ''
		form.author.data = ''
		form.slug.data = ''

		# add post data to database
		db.session.add(post)
		db.session.commit()

		# return a message
		flash('post submitted successfully')


		# redirect a webpage
	return render_template("add_post.html", form = form)

# create json webpage
@app.route('/date')
def get_current_date():
	favorite_pizza = {
		"chris": "pineapple",
		"shannon": "cheese",
		"bill": "sausage"}
	return favorite_pizza
	#return {"date": date.today()}


# create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	email = db.Column(db.String(120), nullable = False, unique = True)
	favorite_color = db.Column(db.String(120))
	date_added = db.Column(db.DateTime, default = datetime.utcnow)
	# password
	password_hash = db.Column(db.String(128))


	@property
	def password(self):
		raise AttributeError('password not readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# create a string
	def __repr__(self):
		return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()
	
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("user deleted")

		our_users = Users.query.order_by(Users.date_added)
		return render_template("add_user.html", 
		form = form, 
		name = name,
		our_users = our_users) 

	except:
		flash("there was a problem deleting user")
		return render_template("add_user.html", 
		form = form, 
		name = name,
		our_users = our_users) 

# create a form class
class UserForm(FlaskForm):
	name = StringField("name?", validators = [DataRequired()])
	email = StringField("email?", validators = [DataRequired()])
	favorite_color = StringField("favorite color?")
	password_hash = PasswordField('password', validators=[DataRequired(), EqualTo('password_hash2', message='password must match')])
	password_hash2 = PasswordField('confirm password', validators=[DataRequired()])
	submit = SubmitField("Submit")


# update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favorite_color = request.form['favorite_color']
		try:
			db.session.commit()
			flash("user updated!")
			return render_template("update.html",
				form = form,
				name_to_update = name_to_update)
		except:
			flash("error!")
			return render_template("update.html",
				form = form,
				name_to_update = name_to_update)
	else:
		return render_template("update.html",
				form = form,
				name_to_update = name_to_update,
				id = id)

# create a form class
class PasswordForm(FlaskForm):
	email = StringField("what's your email?", validators = [DataRequired()])
	password_hash = PasswordField("what's your password?", validators = [DataRequired()])
	submit = SubmitField('submit')


# create a form class
class NamerForm(FlaskForm):
	name = StringField("what's your name?", validators = [DataRequired()])
	submit = SubmitField('submit')


# create a route decorator
#@app.route('/')

#def index():
#	return "<h1>hand stitched cranes</h1>"


@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email = form.email.data).first()
		if user is None:
			# hash password
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(name = form.name.data, email = form.email.data, favorite_color = form.favorite_color.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		form.favorite_color.data = ''
		form.password_hash.data = ''

		flash("user added")
	our_users = Users.query.order_by(Users.date_added)
	return render_template('add_user.html', 
		form = form, 
		name = name,
		our_users = our_users) 
		
@app.route('/')
def index():
	first_name = 'chris'
	stuff = 'a <strong>chinese</strong> inspired blog'
	favorite_pizza = ['peppers', 'pineapple', 'mushroom', 'pesto']
	return render_template('index.html', 
		first_name = first_name,
		stuff = stuff,
		favorite_pizza = favorite_pizza)

# localhost:50000/user/chris
@app.route('/user/<name>')

def user(name):
	return render_template('user.html', user_name = name)

# create custom error pages

# invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# internal server error URL
@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

# create password test page
@app.route('/test_pw', methods = ['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()

	# validate form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# clear the form
		form.name.data = ''
		form.password_hash.data = ''

		pw_to_check = Users.query.filter_by(email=email).first()
		#flash("form submitted successfully!")

	return render_template('test_pw.html',
		email = email,
		password = password,
		pw_to_check = pw_to_check,
		form = form)


# create name page
@app.route('/name', methods = ['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	
	# validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("form submitted successfully!")

	return render_template('name.html',
		name = name,
		form = form)























