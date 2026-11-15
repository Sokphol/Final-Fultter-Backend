import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, subfolder: str = "products") -> str:
    """Save an uploaded file and return its relative URL path."""
    if not file or not allowed_file(file.filename):
        raise ValueError("Invalid file type. Allowed: png, jpg, jpeg, gif, webp")

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return f"/uploads/{subfolder}/{filename}"


def delete_file(file_url: str) -> bool:
    """Delete a file from disk given its URL path."""
    if not file_url:
        return False
    relative = file_url.lstrip("/")
    full_path = os.path.join(os.getcwd(), relative)
    if os.path.exists(full_path):
        os.remove(full_path)
        return True
    return False
