from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.activity import Activity
from app.models.saved_city import SavedCity
from app.models.city import City
from app.models.weather import Weather
from app.core.security import hash_password

def run_seed():
    db = SessionLocal()
    try:
        users = [
            {"name": "Admin", "email": "admin@test.com", "role": UserRole.ADMIN},
            {"name": "Analyst", "email": "analyst@test.com", "role": UserRole.ANALYST},
            {"name": "User", "email": "user@test.com", "role": UserRole.USER},
        ]

        for u in users:
            existing = db.query(User).filter(User.email == u["email"]).first()

            if not existing:
                new_user = User(
                    name=u["name"],
                    email=u["email"],
                    password=hash_password("123456"),
                    role=u["role"],
                )
                db.add(new_user)

        db.commit()
        print(f"Seeding completed.{(users)}, users added.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()