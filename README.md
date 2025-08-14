Install the dependency

sudo apt install python3-pip python3-venv

cd keepalived-dashboard
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

We need to change the Remote Node address and VIP in main.py file.
cd app
vim main.py


keepalived dashboard will be running on 
uvicorn app.main:app --host 0.0.0.0 --port 8080
