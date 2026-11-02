"""REST endpoints for managing accounts."""

import re

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from service.models import Account, db

accounts = Blueprint("accounts", __name__)
ACCOUNT_FIELDS = {"name", "email", "phone_number", "address", "account_type"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _json_object():
    if not request.is_json:
        return None, (jsonify({"error": "Content-Type must be application/json"}), 415)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, (jsonify({"error": "Request body must be a JSON object"}), 400)
    unknown_fields = set(payload) - ACCOUNT_FIELDS
    if unknown_fields:
        return None, (
            jsonify({"error": "Unknown fields", "fields": sorted(unknown_fields)}),
            400,
        )
    return payload, None


def _validate(payload, require_name=False):
    if require_name and not payload.get("name"):
        return "name is required"
    if "name" in payload and (
        not isinstance(payload["name"], str) or not payload["name"].strip()
    ):
        return "name must be a non-empty string"
    if "email" in payload:
        email = payload["email"]
        if not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email):
            return "email must be a valid email address"
    for field in ("phone_number", "address", "account_type"):
        if field in payload and payload[field] is not None and not isinstance(
            payload[field], str
        ):
            return f"{field} must be a string or null"
    return None


@accounts.route("/accounts", methods=["POST"])
def create_account():
    """Create and return an account."""
    payload, error = _json_object()
    if error:
        return error
    validation_error = _validate(payload, require_name=True)
    if validation_error:
        return jsonify({"error": validation_error}), 400
    if not payload.get("email"):
        return jsonify({"error": "email is required"}), 400

    account = Account(**payload)
    db.session.add(account)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An account with this email already exists"}), 409
    return jsonify(account.to_dict()), 201


@accounts.route("/accounts", methods=["GET"])
def list_accounts():
    """Return all accounts ordered by their identifiers."""
    result = Account.query.order_by(Account.id).all()
    return jsonify({"accounts": [account.to_dict() for account in result]})


@accounts.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Return one account or a not-found response."""
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.to_dict())


@accounts.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update the provided fields of an existing account."""
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    payload, error = _json_object()
    if error:
        return error
    validation_error = _validate(payload)
    if validation_error:
        return jsonify({"error": validation_error}), 400
    if not payload:
        return jsonify({"error": "At least one account field is required"}), 400

    for field, value in payload.items():
        setattr(account, field, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An account with this email already exists"}), 409
    return jsonify(account.to_dict())


@accounts.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account and return an empty success response."""
    account = db.session.get(Account, account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    db.session.delete(account)
    db.session.commit()
    return "", 204
