from flask import Blueprint,render_template
from app.services.dashboard_service import total_registered_visitors,attendence_today

home_bp = Blueprint("home",__name__)

@home_bp.route("/")
def home():
    return render_template("index.html",total_visitors=total_registered_visitors(),
                        today_attendance=attendence_today())