from flask import Blueprint,render_template,request
from app.services.capture_service import capture_images
from app.services.embedding_service import generate_embeddings
from app.database import db
from app.models.models import Visitor

register_bp = Blueprint("register",__name__)

@register_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("visitor_name", "").strip()

        if not name:
            return "Invalid visitor name."
        
        existing = Visitor.query.filter_by(name=name).first()

        if existing:
            return f"Visitor '{name}' already exists."
        
        captured = capture_images(name)
        if not captured:
            return "No Image captured."
        
        generated = generate_embeddings(name,overwrite=True)
        if not generated:
            return "Embedding generation failed."
        
        visitor = Visitor(
            name=name,photo_path=f"dataset/{name}/img_001.jpg" #type:ignore
        )

        db.session.add(visitor)
        db.session.commit()
        
        return f"{name} registered successfully!"
    
    return render_template("register.html")
        

