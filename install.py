import os

print('Installing virtual environment and required packages..')
os.system('virtualenv -p python3 venv && venv/bin/pip install -r requirements.txt')

