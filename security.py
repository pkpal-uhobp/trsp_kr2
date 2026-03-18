import uuid

from itsdangerous import Signer



signer = Signer("secret_key")


def sign_token(user_id: str, last_activity_ts: int) -> str:
    payload = f"{user_id}.{last_activity_ts}"
    signed = signer.sign(payload.encode()).decode()

    return signed


def unsign_token(token: str) -> tuple[str, int]:
    unsigned = signer.unsign(token.encode()).decode()

    try:
        user_id_part, ts_part = unsigned.rsplit(".", 1)
    except ValueError:
        raise ValueError("Bad payload")

    try:
        ts = int(ts_part)
    except ValueError:
        raise ValueError("Invalid timestamp")

    try:
        uuid_obj = uuid.UUID(user_id_part)
    except Exception:
        raise ValueError("Invalid user_id format")

    return str(uuid_obj), ts
