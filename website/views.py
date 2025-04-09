from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import DryingRecord

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        user_records = DryingRecord.query.filter_by(user_id=current_user.id).order_by(DryingRecord.timestamp.desc()).all()
        return render_template("records.html", user=current_user, records=user_records)
    else:
        return redirect(url_for('auth.login'))
