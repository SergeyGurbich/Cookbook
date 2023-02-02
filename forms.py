from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, EqualTo, Email

class AddToRecipe(FlaskForm):
  ingredient =  SelectField("Ingredient")
  weight = IntegerField("Weight in gr.", default=100)
  add = SubmitField("Add")

class AddRecipe(FlaskForm):
  title =  StringField("Title", validators=[DataRequired()])
  instructions = TextAreaField("Instructions")
  submit = SubmitField("Confirm!")

class AddProduct(FlaskForm):
  title =  StringField("Name of the product", validators=[DataRequired()])
  calories = IntegerField("Calories per 100 gr.", default=1)
  proteins = FloatField("Proteins per 100 gr.", default=1)
  submit = SubmitField("Confirm!")

class AddMeal(FlaskForm):
  recipe = SelectField("Recipe")
  ingredient=SelectField("Snack")
  weight = IntegerField("Weight in gr.", default=100)
  add_rec = SubmitField("Add meal")
  add_prod=SubmitField("Add snack")
  clean=SubmitField("Clean")

class Search(FlaskForm):
    word=StringField("Search by title", validators=[DataRequired()])
    submit = SubmitField("Search!")

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  #password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

