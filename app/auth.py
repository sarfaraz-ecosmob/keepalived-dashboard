from fastapi import Request
from starlette.responses import RedirectResponse

USERS = {
    "admin": "ecosmob"  # Replace with hashed passwords in real use
}

def authenticate_user(username: str, password: str) -> bool:
    return USERS.get(username) == password

def get_current_user(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse("/", status_code=302)
    return user

