from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db, Bookmark
import validators

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.get("/")
def get_all():
    bookmarks = Bookmark.query.all()
    bookmark_list = []
    for bookmark in bookmarks:
        bookmark_list.append(
            {
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "user_id": bookmark.user_id,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at,
            }
        )

    # Return the list of bookmarks as a JSON response
    return jsonify({"bookmarks": bookmark_list}), 200


@bookmarks.post("/")
@jwt_required()
def create_bookmark():
    current_user = get_jwt_identity()
    data = request.get_json()

    # Extract the 'body' and 'url' from the incoming request data
    body = data.get("body")
    url = data.get("url")

    # Validate that the URL is provided
    if not url:
        return jsonify({"error": "URL is required"}), 400
    if not validators.url(url):
        return jsonify({"error": "URL is invalid"}), 400

    # Create a new bookmark with the user input and current user ID
    new_bookmark = Bookmark(body=body, url=url, user_id=current_user)

    # Add the bookmark to the session and commit to save in the database
    db.session.add(new_bookmark)
    db.session.commit()

    # Return the created bookmark with the generated short URL
    return (
        jsonify(
            {
                "id": new_bookmark.id,
                "user_id": current_user,
                "bookmark": {
                    "body": new_bookmark.body,
                    "url": new_bookmark.url,
                    "short_url": new_bookmark.short_url,
                    "visits": new_bookmark.visits,
                    "created_at": new_bookmark.created_at,
                },
            }
        ),
        201,
    )


@bookmarks.get("/me")
@jwt_required()
def my_bookmark():
    current_user_id = get_jwt_identity()

    # Lấy tất cả các bookmark của user hiện tại
    bookmarks = Bookmark.query.filter_by(user_id=current_user_id).all()

    # Chuyển các đối tượng Bookmark thành dạng dictionary để trả về dưới dạng JSON
    bookmark_list = []
    for bookmark in bookmarks:
        bookmark_list.append(
            {
                "id": bookmark.id,
                "body": bookmark.body,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "user_id": bookmark.user_id,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at,
            }
        )
    # Trả về danh sách bookmark của user hiện tại dưới dạng JSON
    return jsonify({"bookmarks": bookmark_list}), 200


@bookmarks.get("/avc")
def update_bookmarks():
    return jsonify()
