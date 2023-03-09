import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db
from src.accounts.models import UserAccountTable
from src.accounts.token import confirm_token, generate_token
from src.utils.email import send_email

from .forms import LoginForm, RegisterForm

accounts_bp = Blueprint("accounts", __name__)


# route that handles user registration
@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = UserAccountTable(email=form.email.data, password=form.password.data, tokenGenerationTime=datetime.datetime.now(), emailVerificationStatus=False, emailVerifiedTime=None,
                                roleType=form.role.data, is_admin=False)
        db.session.add(user)
        db.session.commit()

        # make the verification token and send the email to the user
        token = generate_token(user.email)
        confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
        html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)

# route that handles user login
@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = UserAccountTable.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


# route that handles confirming the token from email verification
@accounts_bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.emailVerificationStatus:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.home"))
    email = confirm_token(token)
    user = UserAccountTable.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.emailVerificationStatus = True
        user.emailVerifiedTime = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("core.home"))

# route that handles resending the verification email if needed
@accounts_bp.route("/resend")
@login_required
def resend_confirmation():
    if current_user.emailVerificationStatus:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("core.home"))
    token = generate_token(current_user.email)
    confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
    html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("accounts.inactive"))

# route that checks if the user hasn't verified their account yet
@accounts_bp.route("/inactive")
@login_required
def inactive():
    if current_user.emailVerificationStatus:
        return redirect(url_for("core.home"))
    return render_template("accounts/inactive.html")

# route that handles logging out
@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))
