from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameEmailForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired()], render_kw={"type": "email"})
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameEmailForm()
    email_error = None  # Initialize the error variable

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        session['name'] = form.name.data

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            if old_email is not None and old_email != form.email.data:
                flash('Looks like you have changed your email!')

        # Check if the email is a UofT email
        if 'utoronto.ca' not in form.email.data:
            # Set the email error flag but do not redirect
            email_error = "Please use your UofT email."
        else:
            # Only update the session if the email is valid
            session['email'] = form.email.data
            # Redirect only if both name and email are valid
            return redirect(url_for('index'))

    # Render the form with the potential error message
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'),
                           email_error=email_error)
