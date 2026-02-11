"""
One-command launcher: starts FastAPI, Ngrok, and optionally LiveKit agent.
Press Ctrl+C in this window to stop all services.
"""
import os
import sys
import time
import atexit
import subprocess
import webbrowser
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

# Child processes - will be killed on exit
processes = []


def kill_all():
    """Stop all child processes."""
    for p in processes:
        try:
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill()
        except Exception:
            pass
    processes.clear()


def main():
    global processes

    print("")
    print("=" * 55)
    print("  NSOL BPO - One-Command System Start")
    print("=" * 55)
    print("")

    # 1. Start FastAPI (uvicorn)
    print("[1/3] Starting FastAPI server (port 8000)...")
    try:
        p1 = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=ROOT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        processes.append(p1)
        print("      FastAPI started (PID %s)" % p1.pid)
    except Exception as e:
        print("      [ERROR] Failed to start FastAPI: %s" % e)
        return 1

    time.sleep(3)

    # 2. Start Ngrok
    print("[2/3] Starting Ngrok tunnel...")
    try:
        p2 = subprocess.Popen(
            ["ngrok", "http", "8000", "--log=stdout"],
            cwd=ROOT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        processes.append(p2)
        print("      Ngrok started (PID %s)" % p2.pid)
    except FileNotFoundError:
        print("      [WARN] Ngrok not found. Install from https://ngrok.com or run in another terminal.")
    except Exception as e:
        print("      [WARN] Ngrok start failed: %s" % e)
    else:
        time.sleep(2)

    # 3. Open browser
    print("[3/3] Opening dashboard in browser...")
    try:
        time.sleep(2)
        webbrowser.open("http://localhost:8000/frontend/dashboard.html")
        print("      Dashboard opened.")
    except Exception as e:
        print("      [WARN] Could not open browser: %s" % e)

    print("")
    print("=" * 55)
    print("  System is running.")
    print("=" * 55)
    print("")
    print("  Dashboard:  http://localhost:8000/frontend/dashboard.html")
    print("  API Docs:   http://localhost:8000/docs")
    print("  Ngrok UI:   http://localhost:4040 (copy HTTPS URL for calls)")
    print("")
    print("  Press Ctrl+C in this window to STOP all services.")
    print("")

    atexit.register(kill_all)

    # Keep running until Ctrl+C or FastAPI dies
    try:
        while True:
            time.sleep(1)
            if processes and processes[0].poll() is not None:
                print("[ERROR] FastAPI server stopped. Exiting.")
                break
    except KeyboardInterrupt:
        print("")
        print("Stopping all services...")
    finally:
        kill_all()
        print("All stopped. Bye.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
