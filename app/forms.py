from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
import phonenumbers


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

#    def validate_phone(self, phone):
#        try:
#            p = phonenumbers.parse(phone.data)
#            if not phonenumbers.is_valid_number(p):
#                raise ValueError()
#        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
#            raise ValidationError('Invalid phone number')

class AdminEditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    admin = BooleanField('Admin User')
    submit = SubmitField('Submit')

class AdminAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    admin = BooleanField('Admin User')
    submit = SubmitField('Submit')

class NomForm(FlaskForm):
    contract_id = IntegerField('Contract ID', validators=[DataRequired(), Length(min=1, max=8)])
    day_nom_value = IntegerField('Nom in MMBTU', validators=[DataRequired(), Length(min=1, max=8)])
    downstream_contract = IntegerField('Contract ID', validators=[DataRequired(), Length(min=6, max=15)])
    downstream_ba = IntegerField('Downstream BA', validators=[DataRequired(), Length(min=1, max=8)])
    rank = IntegerField('Contract ID', validators=[DataRequired(), Length(min=1, max=2)])
    begin_date = DateField('Begin Date', validators=[DataRequired()])
    end_date = IntegerField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')