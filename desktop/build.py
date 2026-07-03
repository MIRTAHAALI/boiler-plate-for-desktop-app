import os

from app import run, start_static_server


import sys
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
print(PARENT_DIR) 
dist = os.path.join(PARENT_DIR, "frontend/dist") # use this if u are running python .\desktop\build.py 
dist = resource_path("frontend/dist") # use this if u are running python .\desktop\package.py 
print(dist)
start_static_server(dist)

run(
    "http://127.0.0.1:8000",
    debug=False
)