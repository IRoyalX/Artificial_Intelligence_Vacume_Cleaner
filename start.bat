@echo off
echo Please wait...
cd VCS
pip install -r requirements.txt
start http://localhost:5000
cls
python app.py
