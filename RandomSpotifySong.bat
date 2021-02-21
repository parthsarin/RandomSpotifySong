@echo off
python -m venv .env
cd .env/Scripts 
activate 
cd .. 
cd .. 
pip install -r requirements.txt 
python randomsong.py