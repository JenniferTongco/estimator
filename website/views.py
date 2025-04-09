from flask import Blueprint, render_template, redirect, url_for, jsonify
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

@views.route('/api/sync', methods=['POST'])
@login_required
def api_sync():
    try:
        data = request.get_json()

        for record in data.get('records', []):
            new_record = DryingRecord(
                initial_weight=record['initial_weight'],
                temperature=record['temperature'],
                humidity=record['humidity'],
                sensor_value=record['sensor_value'],
                initial_moisture=record['initial_moisture'],
                final_moisture=record['final_moisture'],
                drying_time=record['drying_time'],
                final_weight=record['final_weight'],
                user_id=current_user.id
            )
            db.session.add(new_record)

        db.session.commit()
        return jsonify({"status": "success", "message": "Records synced."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500