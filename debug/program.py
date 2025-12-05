import subprocess
import socket
import sys
import time
import os
import traceback


# ---------------------------------------------------------------
# Log errors when frozen (DMG/.app) so we can debug failures
# ---------------------------------------------------------------
def log_exception():
    """Write crash info to error_log.txt if something fails."""
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())


# ---------------------------------------------------------------
# Return the correct file path whether frozen or source
# ---------------------------------------------------------------
def resource_path(filename):
    """Resolve file paths correctly for PyInstaller."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # directory where bundled files live
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


# ---------------------------------------------------------------
# Check whether port is already in use
# ---------------------------------------------------------------
def is_port_open(port):
    """Return True if something is already listening on the port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False


# ---------------------------------------------------------------
# Start server only if not already running
# ---------------------------------------------------------------
def start_server_if_needed(port):
    """Start collabServer.py only if nothing is using the port."""
    if is_port_open(port):
        print("Server already running — joining session.")
        return

    print("Starting server...")

    server_file = resource_path("collabServer.py")

    if not os.path.exists(server_file):
        raise FileNotFoundError(
            f"ERROR: Could not find server file: {server_file}"
        )

    # macOS & Linux
    if sys.platform != "win32":
        subprocess.Popen(
            ["python3", server_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        # Windows
        subprocess.Popen(
            ["python", server_file],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    # Give server time to boot
    time.sleep(1.0)


# ---------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------
def main():
    SERVER_PORT = 5002

    # 1. Start or connect to server
    start_server_if_needed(SERVER_PORT)

    # 2. Launch the Whiteboard UI
    whiteboard_file = resource_path("WhiteboardUI.py")

    if not os.path.exists(whiteboard_file):
        raise FileNotFoundError(
            f"ERROR: Could not find WhiteboardUI: {whiteboard_file}"
        )

    print("Launching Whiteboard UI...")

    if sys.platform == "win32":
        subprocess.run(["python", whiteboard_file])
    else:
        subprocess.run(["python3", whiteboard_file])


# ---------------------------------------------------------------
# Run with crash logging
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception:
        log_exception()
        raise