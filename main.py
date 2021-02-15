from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create a flask instance
app = Flask(__name__)

# creating secret key HIDE ON GITHUB
app.config['SECRET_KEY'] = "****"

# create a form class
class NamerForm(FlaskForm):
	name = StringField("What's your name?", validators = [DataRequired()])
	submit = SubmitField('Submit')



# create a route decorator
@app.route('/')

#def index():
#	return "<h1>hand stitched cranes</h1>"

def index():
	first_name = 'chris'
	stuff = 'a <strong>chinese</strong> inspired blog'
	favorite_pizza = ['peppers', 'pineapple', 'mushroom', 'pesto']
	return render_template('index.html', 
		first_name=first_name,
		stuff=stuff,
		favorite_pizza=favorite_pizza)

# localhost:50000/user/chris
@app.route('/user/<name>')

def user(name):
	return render_template('user.html', user_name=name)

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
@app.route('/name', methods-['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	return render_template('name.html')
























