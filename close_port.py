import subprocess
import sys
import os
import signal

PORT = "5002"


def kill_process_on_port(port):
    print(f"Scanning for processes using port {port}...")

    if sys.platform == "win32":
        # Windows: use netstat + taskkill
        cmd = f'netstat -ano | findstr :{port}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.stdout.strip() == "":
            print(f"No process is using port {port}.")
            return

        print(result.stdout)

        # Extract PID (last column)
        lines = result.stdout.strip().splitlines()
        pids = set()
        for line in lines:
            parts = line.split()
            pid = parts[-1]
            pids.add(pid)

        for pid in pids:
            print(f"Killing PID {pid}...")
            subprocess.run(f"taskkill /PID {pid} /F", shell=True)
        print("Done.")

    else:
        # macOS / Linux: use lsof
        cmd = ["lsof", "-ti", f"tcp:{port}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout.strip() == "":
            print(f"No process is using port {port}.")
            return

        pids = result.stdout.strip().splitlines()

        for pid in pids:
            print(f"Killing PID {pid}...")
            os.kill(int(pid), signal.SIGKILL)

        print("Done.")


if __name__ == "__main__":
    kill_process_on_port(PORT)