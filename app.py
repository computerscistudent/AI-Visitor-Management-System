from flask import Flask
from app.routes.home import home_bp
from app.routes.register import register_bp
from app.routes.recognize import recognize_bp
from app.routes.attendence import attendence_bp

app = Flask(__name__,template_folder="app/templates")

app.register_blueprint(home_bp)
app.register_blueprint(register_bp)
app.register_blueprint(recognize_bp)
app.register_blueprint(attendence_bp)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)