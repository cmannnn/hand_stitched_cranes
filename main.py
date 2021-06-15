from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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





# create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	email = db.Column(db.String(120), nullable = False, unique = True)
	favorite_color = db.Column(db.String(120))
	date_added = db.Column(db.DateTime, default = datetime.utcnow)

	# create a string
	def __repr__(self):
		return '<Name %r>' % self.name

# create a form class
class UserForm(FlaskForm):
	name = StringField("name?", validators = [DataRequired()])
	email = StringField("email?", validators = [DataRequired()])
	favorite_color = StringField("favorite color")
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
				name_to_update = name_to_update)


# create a form class
class NamerForm(FlaskForm):
	name = StringField("What's your name?", validators = [DataRequired()])
	submit = SubmitField('Submit')

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
			user = Users(name = form.name.data, email = form.email.data, favorite_color = form.favorite_color.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		form.favorite_color.data = ''
		
		flash("User added")
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
























