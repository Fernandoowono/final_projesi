from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin_email = "admin@example.com"
    admin = User.query.filter_by(email=admin_email).first()

    if not admin:
        admin = User(
            email=admin_email,
            password=generate_password_hash("admin123"),
            role="admin",
            name="Admin Kullanıcı"
        )
        db.session.add(admin)
        db.session.commit()
        print("Administrador creado correctamente.")
    else:
        print("Administrador ya existe.")




