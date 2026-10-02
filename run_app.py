import os
import sys
import webbrowser
import threading
import time

# Ensure we run from the correct directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.insert(0, current_dir)

from server import app

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:5000/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "="*65)
    print(" AttendAI &bull; Campus Face Recognition Attendance System")
    print(f" Web Application running at: http://localhost:{port}")
    print(" Press Ctrl+C in terminal to stop server")
    print("="*65 + "\n")
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=port, debug=False)
