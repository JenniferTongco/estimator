from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import DryingRecord, db

# Create a blueprint for the API
api = Blueprint('api', __name__)

# Route to handle syncing data
@api.route('/sync', methods=['POST'])
@login_required  # Ensure the user is logged in
def sync():
    try:
        # Get the data sent from the local app
        data = request.get_json()

        # Loop through each record and insert it into the PostgreSQL database
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

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({"status": "success", "message": "Records synced."}), 200

    except Exception as e:
        # If there's an error, return an error message
        return jsonify({"status": "error", "message": str(e)}), 500
