from flask import Blueprint,render_template,request
from app.services.capture_service import capture_images
from app.services.embedding_service import generate_embeddings

register_bp = Blueprint("register",__name__)

@register_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("visitor_name", "").strip()

        if not name:
            return "Invalid visitor name."
        
        captured = capture_images(name)
        if not captured:
            return "No Image captured."
        
        generated = generate_embeddings(name,overwrite=True)
        if not generated:
            return "Embedding generation failed."
        
        return f"{name} registered successfully!"
    
    return render_template("register.html")
        

