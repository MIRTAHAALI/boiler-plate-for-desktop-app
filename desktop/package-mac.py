import subprocess
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
PARENT_DIR = os.path.dirname(BASE_DIR)
print(PARENT_DIR)
frontend = os.path.join(PARENT_DIR, "frontend")
print(frontend)
try:
    result = subprocess.run(
        ["npm", "run", "build"],   # <-- no .cmd on macOS
        cwd=frontend,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    print('Build complete')
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("Frontend build failed")
except Exception as e:
    print(type(e))
    print(e)
build_file = os.path.join(PARENT_DIR, "desktop/build-mac.py")
dist_folder = os.path.join(PARENT_DIR, "frontend/dist")
result = subprocess.run(
    [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        # "--onefile",
        "--windowed",
        "--name",
        "MyApplication",
        f"--add-data={dist_folder}:frontend/dist",   # <-- colon, not semicolon
        build_file,
    ],
    text=True,
    capture_output=True,
)
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    raise RuntimeError("PyInstaller failed")