from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User


def search_users(
    db: Session,
    current_user_id: str,
    query: str,
    limit: int = 20,
):
    return (
        db.query(User)
        .filter(
            User.id != current_user_id,
            or_(
                User.username.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
            ),
        )
        .order_by(User.username.asc())
        .limit(limit)
        .all()
    )
