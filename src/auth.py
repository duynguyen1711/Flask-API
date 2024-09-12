from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required, get_jwt_identity
import validators.email
from werkzeug.security import check_password_hash,generate_password_hash
import validators
from src.database import User,db
auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")
@auth.post('/register')
def register():
    username = request.json['username']
    email=request.json['email']
    password = request.json['password']
    if len(username) < 6:
        return jsonify({"error":"user more than 6 character"}),400
    if len(password) < 6:
        return jsonify({"error":"password more than 6 character"}),400
    if not username.isalnum() or " " in username:
        return jsonify({"error":"no space in username or num"}),400
    if not validators.email(email):
        return jsonify({"error":"email is invalid"}),400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email đã được sử dụng"}), 409
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "user đã được sử dụng"}), 409
    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {"message":"user created",
        "user":{
            'username':username,'email':email
        }
        }   ),201
@auth.get('/')
def get_all_user():
    users = User.query.all()
    users_list = []

    # Tạo danh sách chứa các thông tin cần trả về
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
        })

    return jsonify({
        "users": users_list 
    }), 200  # Trả về mã trạng thái 200 - OK

@auth.post('/login')
def login():
    email =request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password,password)
        if is_password_correct:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity = user.id)
        return jsonify({
            "refresh":refresh_token,
            "access":access_token,
            "username":user.username,
            "email":user.email
        }),201
    return jsonify({"error":"wrong crendentials"}),401


@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Trả về thông tin user đã xác thực
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }), 200
@auth.post("/token/refresh")
@jwt_required(refresh = True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity = identity)
    return jsonify({
        "acess":access
    }),200