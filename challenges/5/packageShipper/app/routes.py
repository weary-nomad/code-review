from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, flash, session, current_app, g
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, ShippingLabel
from app.forms import LoginForm, RegistrationForm, ShippingForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=False)
            session.permanent = False
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.products')
            return redirect(next_page)
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@main.route('/products')
@login_required
def products():
    return render_template('products.html')

@main.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    form = ShippingForm()
    if form.validate_on_submit():
        label = ShippingLabel(
            user_id=current_user.id,
            customer_name=form.customer_name.data,
            package_type=form.package_type.data,
            destination=form.destination.data
        )
        db.session.add(label)
        db.session.commit()

        return redirect(url_for('main.confirmation', label_id=label.id))

    return render_template('purchase.html', form=form)

@main.route('/confirmation/<int:label_id>')
@login_required
def confirmation(label_id):
    label = ShippingLabel.query.filter_by(id=label_id, user_id=current_user.id).first_or_404()

    template_context = {
        'config': current_app.config,
        'request': request,
        'session': session,
        'g': g
    }
    processed_name = render_template_string(label.customer_name, **template_context)
    label.customer_name = processed_name

    return render_template('confirmation.html', label=label)