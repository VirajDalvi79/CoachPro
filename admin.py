"""
admin.py

Backend for admin/staff authentication. This file was empty in the
uploaded project and Phase 1 ("Admin Login") needs a backend to call,
so this is a new module, not a fix to existing logic — flag it if you
had different plans for it.

Passwords are stored as salted PBKDF2-SHA256 hashes using only the
standard library (no bcrypt/passlib dependency required).
"""


import hashlib
import os
from database import connection, cursor


class Admin:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _hash_password(password, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000
        ).hex()
        return pwd_hash, salt
    

    def admin_exists(self):
     self.cursor.execute("SELECT COUNT(*) FROM admins")
     return self.cursor.fetchone()[0] > 0

    def create_admin(self, username, password, full_name, role="ADMIN"):
        pwd_hash, salt = self._hash_password(password)
        self.cursor.execute(
            """
            INSERT INTO admins (username, password_hash, salt, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, pwd_hash, salt, full_name, role)
        )
        self.connection.commit()

    def authenticate(self, username, password):
        """Returns a dict with admin_id/full_name/role on success, else None."""
        self.cursor.execute(
            """
            SELECT admin_id, password_hash, salt, full_name, role, is_active
            FROM admins
            WHERE username = %s
            """,
            (username,)
        )
        result = self.cursor.fetchone()

        if result is None:
            return None

        admin_id, stored_hash, salt, full_name, role, is_active = result

        if not is_active:
            return None

        computed_hash, _ = self._hash_password(password, salt)

        if computed_hash != stored_hash:
            return None

        return {"admin_id": admin_id, "full_name": full_name, "role": role}

    def change_password(self, admin_id, new_password):
        pwd_hash, salt = self._hash_password(new_password)
        self.cursor.execute(
            """
            UPDATE admins
            SET password_hash = %s, salt = %s
            WHERE admin_id = %s
            """,
            (pwd_hash, salt, admin_id)
        )
        self.connection.commit()

    def deactivate_admin(self, admin_id):
        self.cursor.execute(
            "UPDATE admins SET is_active = 0 WHERE admin_id = %s",
            (admin_id,)
        )
        self.connection.commit()

    def list_admins(self):
        self.cursor.execute(
            """
            SELECT admin_id, username, full_name, role, is_active
            FROM admins
            ORDER BY full_name
            """
        )
        return self.cursor.fetchall()
