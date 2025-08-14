# Keepalived Dashboard

A simple dashboard for monitoring and managing Keepalived.

## 📦 Installation

### 1. Install Dependencies
```bash
sudo apt install python3-pip python3-venv
```

### 2. Clone & Setup Virtual Environment
```bash
cd keepalived-dashboard
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Requirements
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Update the **Remote Node Address** and **VIP** in the `main.py` file:

```bash
cd app
vim main.py
```

Make sure to replace the placeholders with your actual values.

---

## 🚀 Running the Dashboard

Run the Keepalived dashboard using **uvicorn**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Once running, the dashboard will be available at:
```
http://<your-server-ip>:8080
```

To run as a background service (systemd example):
```
sudo tee /etc/systemd/system/keepalived-dashboard.service <<EOF
[Unit]
Description=Keepalived Dashboard
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/keepalived-dashboard
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now keepalived-dashboard
```

---

## 📝 Notes
- Ensure Keepalived is running on your nodes.
- Make sure ports are open in your firewall/security group if accessing remotely.
