from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NomForm, AdminEditUserForm, AddUser
from app.models import User, Company, Contract, Nom
import datetime
from functools import wraps
from app.tables import Users, Noms
import pandas
from pandas import DataFrame



def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == 3:
            return f(*args, **kwargs)
        else:
            return redirect('https://www.youtube.com/watch/dQw4w9WgXcQ')
    return wrap

def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role >= 1:
            return f(*args, **kwargs)
        else:
            return redirect('https://www.youtube.com/watch/dQw4w9WgXcQ')
    return wrap


@app.route('/')
@app.route('/index')
@login_required
def index():
    form = NomForm()
    if form.validate_on_submit():
        for day in range((form.end_date.data - form.begin_date.data).days + 1):
            day_delta = datetime.timedelta(days=1)
            date = (form.begin_date.data + (day * day_delta))
            old_nom = Nom.query.filter_by(contract_id=form.contract_id.data, downstream_contract=form.downstream_contract.data, downstream_ba=form.downstream_ba.data, day_nom=date, rank=form.rank.data).first()
            if old_nom is not None:
                old_nom.contract_id = form.contract_id.data
                old_nom.day_nom_value = form.day_nom_value.data
                old_nom.downstream_contract = form.downstream_contract.data
                old_nom.downstream_ba = form.downstream_ba.data
                old_nom.day_nom = date
                old_nom.rank = form.rank.data
                old_nom.delivery_id = form.delivery_id.data
                old_nom.edit = True
                old_nom.published_time = datetime.datetime.utcnow()
                db.session.commit()
            else:
                post = Nom(contract_id=form.contract_id.data, user=current_user.username, day_nom_value=form.day_nom_value.data, downstream_contract=form.downstream_contract.data, downstream_ba=form.downstream_ba.data, rank=form.rank.data, day_nom=date, delivery_id=form.delivery_id.data)
                db.session.add(post)
                db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template("index.html", title='Nominations', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['username'] = form.username.data
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.title = form.title.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.title.data = current_user.title
        form.phone.data = current_user.phone
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/admin')
@login_required
@admin_required
def admin():
    company = Contract.query.filter_by(producer=current_user.company).all()
    if len(company) == 0:
        company = Contract.query.filter_by(marketer=current_user.company).all()

    for companies in company:
        contract = companies.contract_id
    


    return render_template('admin.html', title='Admin', noms=noms)

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    form = NomForm()
    if current_user.role >= 2:
        contract = Contract.query.all()
    elif Contract.query.filter_by(producer=current_user.company).first() is not None:
        contract = Contract.query.filter_by(producer=current_user.company).all()
    elif Contract.query.filter_by(marketer=current_user.company).first() is not None:
        contract = Contract.query.filter_by(marketer=current_user.company).all()
    contracts = []

    for i in contract:
        contracts.append(i.contract_id)

    noms = Nom.query.filter(Nom.contract_id.in_(contracts)).statement

    df = pandas.read_sql(noms, db.engine)
    df['day_nom'] = df['day_nom'].dt.strftime('%m/%d/%Y')

    df['Day'] = df['day_nom']
    df['Contract ID'] = df['contract_id']
    df['Downstream Contract'] = df['downstream_contract']
    df['Downstream BA'] = df['downstream_ba']
    df['Rank'] = df['rank']
    df['Delivery ID'] = df['delivery_id']
    df = df.pivot_table(columns=['Contract ID','Delivery ID'], index='Day', values='day_nom_value', aggfunc='sum')
    df = df.fillna(0)
    df = df.reset_index()
    df = df.to_html(index=False)
    if not contract:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Noms(df)
        table.border = True
    return render_template('admin_dashboard.html', title='Admin Dashboard', table=df)

@app.route('/nominate', methods=['GET', 'POST'])
@login_required
@user_required
def nominate():
    form = NomForm()
    if form.validate_on_submit():
        for day in range((form.end_date.data - form.begin_date.data).days + 1):
            day_delta = datetime.timedelta(days=1)
            date = (form.begin_date.data + (day * day_delta))
            old_nom = Nom.query.filter_by(contract_id=form.contract_id.data, downstream_contract=form.downstream_contract.data, downstream_ba=form.downstream_ba.data, day_nom=date, rank=form.rank.data).first()
            if old_nom is not None:
                old_nom.contract_id = form.contract_id.data
                old_nom.day_nom_value = form.day_nom_value.data
                old_nom.downstream_contract = form.downstream_contract.data
                old_nom.downstream_ba = form.downstream_ba.data
                old_nom.day_nom = date
                old_nom.rank = form.rank.data
                old_nom.delivery_id = form.delivery_id.data
                old_nom.edit = True
                old_nom.published_time = datetime.datetime.utcnow()
                db.session.commit()
            else:
                post = Nom(contract_id=form.contract_id.data, user=current_user.username, day_nom_value=form.day_nom_value.data, downstream_contract=form.downstream_contract.data, downstream_ba=form.downstream_ba.data, rank=form.rank.data, day_nom=date, delivery_id=form.delivery_id.data)
                db.session.add(post)
                db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template("nominate.html", title='Nominations', form=form)

@app.route('/admin/user_management')
@login_required
@admin_required
def user_management():
    user = User.query.all()
    if not user:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Users(user)
        table.border = True
    return render_template('user_management.html', title='User Management', table=table)

@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(id):
    user = User.query.filter_by(id=id).first()
    form = AdminEditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.title = form.title.data
        user.phone = form.phone.data
        user.role = form.permission.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user_management'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.title.data = user.title
        form.phone.data = user.phone
        form.permission.data = user.role
    return render_template('edit_user.html', form=form)


@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AddUser()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, company=form.company.data, title=form.title.data, role=form.role.data, phone=form.phone.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash('New user has been registered!')
        return redirect(url_for('user_edit'))
    return render_template('add_user.html', title='Add User', form=form)