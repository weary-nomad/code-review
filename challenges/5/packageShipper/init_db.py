from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if users already exist
    if User.query.count() == 0:
        # Create user account
        user = User(email='user@example.com', role='user')
        user.set_password('SecurePass123!')
        db.session.add(user)

        # Create admin account
        admin = User(email='admin@example.com', role='admin')
        admin.set_password('AdminSecure456!')
        db.session.add(admin)

        db.session.commit()
        print("Database initialized with test accounts:")
        print("User: user@example.com / SecurePass123!")
        print("Admin: admin@example.com / AdminSecure456!")
    else:
        print("Database already contains users, skipping initialization.")

if __name__ == '__main__':
    print("Initializing database...")