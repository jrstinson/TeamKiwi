"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import BooleanField, validators
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import FileField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)

class UploadForm(Form):
    url = TextField('', [InputRequired()])


    def clean_url(self, url):
        return clean_url(url)



class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')
    image = FileField()


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


"""
    Written by: Nick Peace
    Registration Form - Creates the registration form with appropriate validators 
"""
class RegistrationForm(Form):
    user = StringField('Username', [
        validators.Length(min=5, max=20, message="Your username must be anywhere from 5 to 20 characters in length")])
    password = PasswordField('Password', [validators.DataRequired(), validators.equal_to('confirmPassword',
                                                                                         message="Passwords do not match, try again")])
    confirmPassword = PasswordField('Confirm Password')
    fullName = StringField('Full Name', [validators.Length(min=0, max=50)])
    email = StringField('Email', [validators.Email(message="Must enter a vaild email.")])
    bio = StringField('Bio',[validators.Length(min=0, max=250,message="Keep your bio short and sweet! No more than 250 characters.")])
    favoriteLanguages = StringField('Favorite Languages',[validators.Length(min=0, max=250,message="Keep your languages short and sweet! No more than 250 characters.")])
