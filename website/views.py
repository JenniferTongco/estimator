from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import DryingRecord

views = Blueprint('views', __name__)

@views.route('/records')
@login_required
def records():
    user_records = DryingRecord.query.filter_by(user_id=current_user.id).order_by(DryingRecord.timestamp.desc()).all()
    return render_template("records.html", user=current_user, records=user_records)
