from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from ..email import send_email
from .forms import Form1
from .. import db
from ..models import User, Role

@main.route('/', methods=['GET', 'POST'])
def index():
    form = Form1()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # create the user if he does not exist and assign a role to him/her
            user_role = Role.query.filter_by(name='User').first()
            user = User(username = form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # send email
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New user', 'mail/new_user', user = user)
            flash('You has been registered')
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())