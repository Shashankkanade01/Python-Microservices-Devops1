import time
import os

LOG_FILE = "/logs/app.log"  # backend writes here
os.makedirs("/logs", exist_ok=True)

def log_writer():
    print("Logger started, reading backend logs...")
    last_size = 0
    while True:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                f.seek(last_size)  # start reading from last position
                new_lines = f.readlines()
                if new_lines:
                    for line in new_lines:
                        print("LOG:", line.strip())
                last_size = f.tell()
        time.sleep(5)

if __name__ == "__main__":
    log_writer()
