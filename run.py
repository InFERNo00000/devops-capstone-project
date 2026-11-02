"""Development entry point for the Accounts service."""

import os

from service import create_app
from service.models import db

app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
