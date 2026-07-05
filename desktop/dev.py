import os
import subprocess
import socket
import time
import shutil
from app import run


import platform
npm_cmd = 'npm.cmd'
os_name = platform.system()

if os_name == 'Windows':
    npm_cmd = 'npm.cmd'
    print("You are using Windows.")
elif os_name == 'Darwin':
    npm_cmd = 'npm'
    print("You are using macOS.")
else:
    print(f"You are using another operating system: {os_name}")

# frontend = os.path.abspath("../frontend")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

PARENT_DIR = os.path.dirname(BASE_DIR)
print(PARENT_DIR)
frontend = os.path.join(PARENT_DIR, "frontend")
print(frontend)

print("Frontend path:", frontend)
print("Exists:", os.path.exists(frontend))
print("Is dir:", os.path.isdir(frontend))

print("npm:", shutil.which("npm"))
print("npm.cmd:", shutil.which("npm.cmd"))
vite = None
try:
    vite = subprocess.Popen(
    [npm_cmd, "run", "dev"],
    cwd=frontend,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

except Exception as e:
    print(type(e))
    print(e)

def wait_for_port(port):
    while True:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1)
            return
        except OSError:
            time.sleep(0.5)



# run("http://localhost:5173", debug=True)

# print('Please wait to close')
# vite.terminate()
# print('Closed')
from app import start_media_server
start_media_server(port=8000)   # <-- add this before run()

try:
    
    run("http://localhost:5173", debug=True)
except KeyboardInterrupt:
    print("\nKeyboardInterrupt caught. Shutting down...")
finally:
    print('Please wait to close...')
    if vite is not None:
        if os.name == 'nt':
            # On Windows, npm.cmd spawns a child node.exe process.
            # We must kill the entire process tree, otherwise node.exe stays alive and holds the port.
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(vite.pid)], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
        else:
            # Fallback for Unix/Linux/Mac
            vite.terminate()
            vite.wait()
    print('Closed')