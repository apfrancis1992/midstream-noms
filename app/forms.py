from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Permissions, Contract, Delivery
import phonenumbers
from flask_login import current_user


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


class AdminAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    admin = BooleanField('Admin User')
    submit = SubmitField('Submit')

class NomForm(FlaskForm):
    contract_id = SelectField('Contract ID', coerce=int)
    delivery_id = SelectField('Delivery Point')
    day_nom_value = IntegerField('Nom in MMBTU', validators=[DataRequired()])
    downstream_contract = IntegerField('Downstream Contract', validators=[DataRequired()])
    downstream_ba = IntegerField('Downstream BA', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired()])
    begin_date = DateField('Begin Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self):
        super(NomForm, self).__init__()
        self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.filter_by(producer=current_user.company).all()]
        self.delivery_id.choices = [(d.delivery_id, d.delivery_name) for d in Delivery.query.all()]


class AdminEditUserForm(FlaskForm):
    access_types = [('3', 'Admin'), ('1', 'User'), ('2', 'Employee')
                   ]
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    permission = SelectField("Permissions", choices=access_types)
    submit = SubmitField('Submit')