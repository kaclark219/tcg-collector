import base64
import hashlib
import hmac
import os
from uuid import UUID

from psycopg.errors import UniqueViolation

from app.core.db import get_db_connection
from app.schemas.profiles import Profile

PIN_HASH_ITERATIONS = 390000
FALLBACK_BINDER_NAME = "Unassigned"


class InvalidPinError(ValueError):
    pass


class AuthenticationError(ValueError):
    pass


class ProfileAlreadyExistsError(ValueError):
    pass


def _validate_pin(pin: str) -> None:
    if len(pin) != 6 or not pin.isdigit():
        raise InvalidPinError("PIN must be exactly 6 digits.")


def hash_pin(pin: str) -> str:
    _validate_pin(pin)
    salt = os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        PIN_HASH_ITERATIONS,
    )
    return (
        f"pbkdf2_sha256${PIN_HASH_ITERATIONS}$"
        f"{base64.b64encode(salt).decode('utf-8')}$"
        f"{base64.b64encode(derived_key).decode('utf-8')}"
    )


def verify_pin(pin: str, encoded_hash: str) -> bool:
    _validate_pin(pin)
    algorithm, iteration_string, salt_b64, hash_b64 = encoded_hash.split("$", 3)
    if algorithm != "pbkdf2_sha256":
        return False

    salt = base64.b64decode(salt_b64.encode("utf-8"))
    expected_hash = base64.b64decode(hash_b64.encode("utf-8"))
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        int(iteration_string),
    )
    return hmac.compare_digest(derived_key, expected_hash)


def _ensure_system_binder(cursor, profile_id: UUID) -> None:
    cursor.execute(
        """
        insert into public.binders (profile_id, name, description, is_system)
        select %s, %s, %s, true
        where not exists (
          select 1
          from public.binders
          where profile_id = %s and is_system = true
        )
        """,
        (
            str(profile_id),
            FALLBACK_BINDER_NAME,
            "Default fallback binder for unassigned cards.",
            str(profile_id),
        ),
    )


def create_profile(username: str, pin: str) -> Profile:
    _validate_pin(pin)
    hashed_pin = hash_pin(pin)

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    insert into public.profiles (username, pin_hash)
                    values (%s, %s)
                    returning id, username
                    """,
                    (username.strip(), hashed_pin),
                )
                row = cursor.fetchone()
                _ensure_system_binder(cursor, row["id"])
            connection.commit()
    except UniqueViolation as exc:
        raise ProfileAlreadyExistsError("Username already exists.") from exc

    return Profile(id=row["id"], username=row["username"])


def login_profile(username: str, pin: str) -> Profile:
    _validate_pin(pin)
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select id, username, pin_hash
                from public.profiles
                where username = %s
                limit 1
                """,
                (username.strip(),),
            )
            row = cursor.fetchone()
            if row is None or not verify_pin(pin, row["pin_hash"]):
                raise AuthenticationError("Invalid username or PIN.")
            _ensure_system_binder(cursor, row["id"])
        connection.commit()

    return Profile(id=row["id"], username=row["username"])

