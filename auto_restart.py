import subprocess
import time
import sys


def run_server():
    while True:
        print("Starting the server...")
        process = subprocess.Popen([sys.executable, "metrics_server.py"])
        process.wait()
        print("Server stopped. Restarting in 5 seconds...")
        time.sleep(5)


if __name__ == "__main__":
    run_server()
