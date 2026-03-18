import time
import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi.params import Query, Depends, Header

from dependencies import get_current_user, get_common_headers
from mock import sample_products, sessions, users_db
from models import UserCreateSchema, UserLoginSchema, UserProfileSchema, CommonHeaders
from security import sign_token

app = FastAPI()


# 3.1
@app.post("/create_user")
async def create_user(
        user_data: UserCreateSchema
):
    return user_data


# 3.2
@app.get("/products/search")
async def search_products(
        keyword: str,
        limit: Annotated[int, Query(ge=1)] = 10,
        category: str | None = None,
):
    results = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category is None or product["category"].lower() == category.lower():
                results.append(product)
    return results[:limit]


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


# 5.1-5.3
@app.post("/login")
async def login(
        login_data: UserLoginSchema,
        response: Response
):
    user = users_db.get(login_data.username)

    if not user or user["password"] != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_id = str(uuid.uuid4())
    now_ts = int(time.time())

    sessions[user_id] = {"username": login_data.username, "last_activity": now_ts}

    token = sign_token(user_id, now_ts)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=300,
        path="/"
    )

    return {"msg": "ok"}


@app.get("/profile")
async def profile(
        username: Annotated[str, Depends(get_current_user)]
):
    user = users_db.get(username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserProfileSchema(username=username, email=user["email"], full_name=user["full_name"])




#5.4-5.5
@app.get("/headers")
async def read_headers(
    common: Annotated[CommonHeaders, Depends(get_common_headers)]
):

    return {
        "User-Agent": common.user_agent,
        "Accept-Language": common.accept_language,
    }


@app.get("/info")
async def info(
    response: Response,
    common: Annotated[CommonHeaders, Depends(get_common_headers)]

):

    server_time = datetime.now(timezone.utc).isoformat()

    response.headers["X-Server-Time"] = server_time

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "User-Agent": common.user_agent,
        "Accept-Language": common.accept_language,
    }
