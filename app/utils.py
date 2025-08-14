import subprocess
import socket

def get_vip_status(vip: str) -> str:
    try:
        result = subprocess.check_output(["ip", "addr"], text=True)
        return "Present" if vip in result else "Not Present"
    except subprocess.CalledProcessError:
        return "Error checking VIP"

def get_hostname():
    return socket.gethostname()

def get_interface_status(interface="eth0"):
    try:
        output = subprocess.check_output(["ip", "link", "show", interface], text=True)
        if "state UP" in output:
            return "UP"
        elif "state DOWN" in output:
            return "DOWN"
        else:
            return "UNKNOWN"
    except Exception as e:
        return f"Error: {e}"

def get_keepalived_role():
    try:
        output = subprocess.check_output(["systemctl", "status", "keepalived"], text=True)
        if "MASTER" in output:
            return "MASTER"
        elif "BACKUP" in output:
            return "BACKUP"
        elif "running" in output:
            return "RUNNING"
        else:
            return "INACTIVE"
    except Exception as e:
        return f"Error: {e}"

def read_keepalived_config(path="/etc/keepalived/keepalived.conf"):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Configuration file not found."

