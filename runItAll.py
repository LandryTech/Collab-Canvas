import subprocess
import time
import sys

# Start server in background
if sys.platform == "win32":
    subprocess.Popen(["python", "serverTest.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
else:
    subprocess.Popen(["python", "serverTest.py"])

# Give server time to start
time.sleep(2)

# Run whiteboard UI
subprocess.run(["python", "WhiteboardUI.py"])