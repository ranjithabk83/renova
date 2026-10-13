import sqlite3
import hashlib
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200_000
        )

        return secrets.compare_digest(
            password_hash.hex(),
            hash_hex
        )

    except Exception:
        return False


def create_user(username, password):
    username = username.strip()

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    try:
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users(username, password_hash)
            VALUES (?, ?)
            """,
            (username, hash_password(password))
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    except Exception as e:
        return False, str(e)


def authenticate_user(username, password):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    user_id, username, password_hash = row

    if verify_password(password, password_hash):
        return {
            "id": user_id,
            "username": username
        }

    return None


def add_project(user_id, project_name, file_name, file_path):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO projects(
            user_id,
            project_name,
            file_name,
            file_path
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            project_name,
            file_name,
            file_path
        )
    )

    conn.commit()
    conn.close()


def get_user_projects(user_id):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            project_name,
            file_name,
            file_path,
            uploaded_at
        FROM projects
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return rows
