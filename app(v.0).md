from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["myApp"]
users = db["users"]

# Helper: role check
def role_required(allowed_roles):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = users.find_one({"_id": ObjectId(user_id)})
            if not user or user.get("role") not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator

# Route: Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user_id = users.insert_one({
        "username": data["username"],
        "password": hashed_pw,
        "role": data.get("role", "user")
    }).inserted_id
    return jsonify({"msg": "User created", "user_id": str(user_id)})

# Route: Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"username": data["username"]})
    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        token = create_access_token(identity=str(user["_id"]))
        return jsonify(access_token=token)
    return jsonify({"error": "Invalid credentials"}), 401

# Route: Change Role (admin only)
@app.route("/users/<user_id>/role", methods=["PUT"])
@role_required(["admin"])
def change_role(user_id):
    data = request.json
    new_role = data.get("role")
    users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": new_role}})
    return jsonify({"msg": "Role updated"})

# Protected Route: Admin-only
@app.route("/admin-only", methods=["GET"])
@role_required(["admin"])
def admin_dashboard():
    return jsonify({"msg": "Welcome, Admin!"})

# Protected Route: Editors
@app.route("/edit-zone", methods=["GET"])
@role_required(["admin", "editor"])
def editor_zone():
    return jsonify({"msg": "Hello, editor or admin"})

if __name__ == "__main__":
    app.run(debug=True)
