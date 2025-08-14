from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.auth import authenticate_user, get_current_user
from app.utils import (
    get_vip_status,
    read_keepalived_config,
    get_hostname,
    get_interface_status,
    get_keepalived_role
)
import requests

# Set remote HAProxy node IP here
REMOTE_NODE_IP = "10.200.10.120"  # change to the second HAProxy node IP

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session['user'] = username
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: str = Depends(get_current_user)):
    local_info = system_info()
    try:
        remote_info = requests.get(f"http://{REMOTE_NODE_IP}:8080/api/system", timeout=2).json()
    except Exception as e:
        remote_info = {"error": str(e)}

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "local_info": local_info,
        "remote_info": remote_info,
        "keepalived_conf": read_keepalived_config()
    })


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.get("/api/system")
def system_info():
    return {
        "hostname": get_hostname(),
        "vip_status": get_vip_status("10.200.10.121"),
        "interface": "eth0",
        "interface_status": get_interface_status("eth0"),
        "keepalived_role": get_keepalived_role()
    }

