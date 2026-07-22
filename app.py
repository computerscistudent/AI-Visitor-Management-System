from flask import Flask , send_from_directory
from app.routes.home import home_bp
from app.routes.register import register_bp
from app.routes.recognize import recognize_bp
from app.routes.attendence import attendence_bp
import os
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from app.database import db
from app.models.models import Visitor,Attendance


app = Flask(__name__,template_folder="app/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(register_bp)
app.register_blueprint(recognize_bp)
app.register_blueprint(attendence_bp)

@app.route("/dataset/<person>/<filename>")
def dataset_image(person,filename):
    return send_from_directory(os.path.join('app','dataset',person),filename)

if __name__ == "__main__":
    with app.app_context():
        print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])

        print("Tables before create:", db.metadata.tables.keys())

        db.create_all()

        print("Tables after create:", db.metadata.tables.keys())

        print("Engine:", db.engine)

        print("✅ Database Connected Successfully!")
    app.run(debug=False, use_reloader=False)