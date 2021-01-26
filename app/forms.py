from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Permissions, Contract, Delivery, Company, Nom
import phonenumbers
from flask_login import current_user
import datetime


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


class AddUser(FlaskForm):
    access_types = [('3', 'Admin'), ('1', 'User'), ('2', 'Employee')]
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    company = SelectField('Company')
    phone = StringField('Phone')
    title = StringField('Title', validators=[DataRequired()])
    role = SelectField('User Role', choices=access_types)
    submit = SubmitField('Submit')

    def __init__(self):
        super(AddUser, self).__init__()
        self.company.choices = [(e.company_name, e.company_name) for e in Company.query.all()]

class NomForm(FlaskForm):
    contract_id = SelectField('Contract ID', coerce=int)
    delivery_id = SelectField('Delivery Point')
    day_nom_value = IntegerField('Nom in MMBTU', validators=[DataRequired()])
    downstream_contract = IntegerField('Downstream Contract', validators=[DataRequired()])
    downstream_ba = IntegerField('Downstream BA', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired()])
    begin_date = DateField('Begin Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_begin_date(form, field):
        if field.data < datetime.date.today() and current_user.role == 1:
            raise ValidationError('Start date cannot be in the past.')

    def validate_end_date(form, field):
        if field.data < form.begin_date.data:
            raise ValidationError('End date must not be earlier than start date.')

    def __init__(self):
        super(NomForm, self).__init__()
        if current_user.role >= 2:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.all()]
        elif Contract.query.filter_by(producer=current_user.company).first() is not None:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.filter_by(producer=current_user.company).all()]
        elif Contract.query.filter_by(marketer=current_user.company).first() is not None:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.filter_by(marketer=current_user.company).all()]

        self.delivery_id.choices = [(d.delivery_id, d.delivery_name) for d in Delivery.query.all()]



class AdminEditUserForm(FlaskForm):
    access_types = [('1', 'User'), ('2', 'Employee'), ('3', 'Admin')
                   ]
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    company = SelectField('Company')
    phone = StringField('Phone', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    permission = SelectField("Permissions", choices=access_types)
    submit = SubmitField('Submit')

    def __init__(self):
        super(AdminEditUserForm, self).__init__()
        self.company.choices = [(c.company_name, c.company_name) for c in Company.query.all()]

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class EditCompanyForm(FlaskForm):
    company = [('producer', 'Producer'), ('marketer', 'Marketer')
                   ]
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_type = SelectField('Company Type', choices=company)
    status = BooleanField('Active')
    submit = SubmitField('Submit')


class EditContractForm(FlaskForm):
    contract_id = IntegerField('Contract Number', validators=[DataRequired()])
    producer = SelectField('Producer')
    marketer = SelectField('Marketer')
    contract_type = StringField('Contract Type', validators=[DataRequired()])
    day_due = IntegerField('Day Due', validators=[DataRequired()])
    active = BooleanField('Active')
    submit = SubmitField('Submit')

    def __init__(self):
        super(EditContractForm, self).__init__()
        self.producer.choices = [(c.company_name, c.company_name) for c in Company.query.filter_by(company_type='producer').order_by(Company.company_name).all()]
        self.marketer.choices = [('', "---")] + [(c.company_name, c.company_name) for c in Company.query.filter_by(company_type='marketer').order_by(Company.company_name).distinct().all()]

class AddUpdateForm(FlaskForm):
    update_title = StringField('Title', validators=[DataRequired(), Length(min=1, max=50)])
    update = TextAreaField('Update', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')

class ConfirmSearchForm(FlaskForm):
    contract_id = SelectField('Contract ID', coerce=int)
    begin_date = DateField('Begin Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self):
        super(ConfirmSearchForm, self).__init__()
        self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Nom.query.order_by(Nom.contract_id).distinct(Nom.contract_id)]


class DashboardSearchForm(FlaskForm):
    contract_id = SelectField('Contract ID', coerce=int)
    begin_date = DateField('Begin Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self):
        super(DashboardSearchForm, self).__init__()
        if current_user.role >= 2:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.order_by(Contract.contract_id).all()]
        elif Contract.query.filter_by(producer=current_user.company).first() is not None:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.filter_by(producer=current_user.company).order_by(Contract.contract_id).all()]
        elif Contract.query.filter_by(marketer=current_user.company).first() is not None:
            self.contract_id.choices = [(c.contract_id, c.contract_id) for c in Contract.query.filter_by(marketer=current_user.company).order_by(Contract.contract_id).all()]