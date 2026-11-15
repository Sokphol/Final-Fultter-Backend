from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return generate_password_hash(plain_password, method="pbkdf2:sha256")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a plain-text password against its hash."""
    return check_password_hash(hashed, plain_password)
