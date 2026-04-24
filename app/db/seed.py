from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.activity import Activity
from app.models.saved_city import SavedCity
from app.models.city import City
from app.models.weather import Weather
from app.core.security import hash_password

def run_seed():
    db = SessionLocal()
    created_users = []
    try:
        users = [
            {"name": "Admin", "email": "admin@test.com", "role": UserRole.ADMIN},
            {"name": "Analyst", "email": "analyst@test.com", "role": UserRole.ANALYST},
            {"name": "User", "email": "user@test.com", "role": UserRole.USER},
        ]
        default_password = "123456"

        for u in users:
            existing = db.query(User).filter(User.email == u["email"]).first()

            if not existing:
                new_user = User(
                    name=u["name"],
                    email=u["email"],
                    password=hash_password(default_password),
                    role=u["role"],
                )
                db.add(new_user)
                db.flush()

                created_users.append({
                    "id": new_user.id,
                    "email": new_user.email,
                    "role": new_user.role.value,
                    "password": default_password
                })

        db.commit()

        print("\n=== Seeded Users ===")
        for user in created_users:
            print(user)

    finally:
        db.close()