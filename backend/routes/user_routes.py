import re

from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signin", methods=["POST"])
def sign_in(username, password, email, name , surname):

    if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", email):
        return make_response(jsonify({"message": "Invalid email"}), 401)

    try:

    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 401)

    return make_response(jsonify({"message": "User created successfully"}), 201)

@auth_bp.route("/login", methods=["POST"])
@jwt_required()
def login():
    data = request.get_json()

    if not data:
        return make_response(jsonify({"message": "No data provided"}), 401)

    username, password = data.get("username"), data.get("password")



    return

