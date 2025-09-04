
import os
import hashlib

MYSQL_HOST = os.getenv("DATABASE_HOST")
MYSQL_PORT = 3306
MYSQL_AUTH = "root:password"

IMAGE_STORE = "./images"

ADMIN_TOKEN = os.getenv("ADMIN_PASSWORD") or "kxpage-password"
PUBLIC_PREFIX = os.getenv("PUBLIC_PREFIX") or "/kx-api/v1"

def get_admin_hash() -> str:
    h = hashlib.sha512()
    h.update(ADMIN_TOKEN.encode())
    return h.hexdigest()

ADMIN_HASH = get_admin_hash()
