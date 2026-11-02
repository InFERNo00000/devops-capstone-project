"""Database models for the Accounts service."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    """A customer account managed by the service."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    phone_number = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    account_type = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        """Return the public JSON representation of this account."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "account_type": self.account_type,
            "date_joined": self.date_joined.isoformat(),
        }

    def __repr__(self):
        return f"<Account {self.id}: {self.email}>"
