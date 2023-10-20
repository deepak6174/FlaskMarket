from market import app, db
from flask import render_template, jsonify, redirect, url_for, flash
from market.models import Item, Users
from market.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():  # put application's code here
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data,
                               email_address=form.email_address.data,
                               password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: { attempted_user.username }', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Incorrect Username or Password!', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You are logged out!', category='info')
    return render_template('home.html')


@app.route('/purchase/<int:item_id>')
def purchase(item_id: int):
    item = Item.query.filter_by(id=item_id).first()
    if item.price <= current_user.budget:
        current_user.budget -= item.price
        item.owner = current_user.id
        db.session.commit()
        flash(f'{item.name} is purchased in {item.price}$', category='success')
    else:
        flash(f'{item.name} is greater than total budget', category='danger')

    return redirect(url_for('market_page'))


