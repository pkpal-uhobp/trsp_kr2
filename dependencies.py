import time
from typing import Annotated

from fastapi import HTTPException, Request, Response
from fastapi.params import Depends, Header
from itsdangerous import BadSignature

from mock import sessions
from security import unsign_token, sign_token
from models import CommonHeaders


def get_token(request: Request) -> str:
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=401, detail="token not found"
        )

    return token


def get_current_user(
        token: Annotated[str, Depends(get_token)],
        response: Response
) -> str:
    try:
        user_id, ts_in_cookie = unsign_token(token)
    except (BadSignature, ValueError):
        raise HTTPException(status_code=401, detail="Invalid session")

    session = sessions.get(user_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    server_last_activity = int(session.get("last_activity", 0))

    if ts_in_cookie != server_last_activity:
        raise HTTPException(status_code=401, detail="Invalid session")

    now = int(time.time())
    elapsed = now - server_last_activity

    if elapsed >= 300:
        sessions.pop(user_id, None)
        raise HTTPException(status_code=401, detail="Session expired")

    if 180 <= elapsed < 300:
        new_ts = now
        session["last_activity"] = new_ts
        new_token = sign_token(user_id, new_ts)

        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=300,
            path="/"
        )

    return session["username"]

def get_common_headers(
    user_agent: Annotated[str, Header(alias="User-Agent")] = None,
    accept_language: Annotated[str, Header(alias="Accept-Language")] = None
) -> CommonHeaders:

    missing = []
    if not user_agent:
        missing.append("User-Agent")
    if not accept_language:
        missing.append("Accept-Language")

    if missing:
        raise HTTPException(
            status_code=400,
            detail={"message": f"Missing headers: {', '.join(missing)}"}
        )

    return CommonHeaders(user_agent=user_agent, accept_language=accept_language)