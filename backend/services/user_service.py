from sqlalchemy.orm import Session

from backend.core.security import get_password_hash, verify_password
from backend.database.models import User, UserSettings
from backend.repositories.user_repository import UserRepository
from backend.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UserRepository(db)

    def register(self, payload: UserCreate) -> User:
        user = self.repository.get_by_email(payload.email)
        if user:
            raise ValueError("Email already registered")

        created_user = self.repository.create(
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            full_name=payload.full_name,
        )
        self._create_default_settings(created_user.id)
        return created_user

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.repository.get_by_email(email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def _create_default_settings(self, user_id: int) -> None:
        settings = UserSettings(user_id=user_id)
        self.db.add(settings)
        self.db.commit()
