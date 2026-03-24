import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- WSL COMPATIBLE CONFIGURATION ---
# In WSL, "C:\" becomes "/mnt/c/"
WATCH_PATH = r"/mnt/c/Users/Admin/Desktop/Downloads" 

DESTINATIONS = {
    # 1. Coding & Development
    "CODING": r"/mnt/c/Users/Admin/Desktop/Downloads/Code",
    ".js": "CODING", ".jsx": "CODING", ".ts": "CODING", ".tsx": "CODING",
    ".py": "CODING", ".cpp": "CODING", ".c": "CODING", ".cs": "CODING",
    ".html": "CODING", ".css": "CODING", ".json": "CODING", ".env": "CODING",

    # 2. Audio & Music
    "MUSIC": r"/mnt/c/Users/Admin/Desktop/Downloads/Music_Production",
    ".wav": "MUSIC", ".mp3": "MUSIC", ".flac": "MUSIC", ".mid": "MUSIC", ".midi": "MUSIC",

    # 3. Images & Design
    "DESIGN": r"/mnt/c/Users/Admin/Desktop/Downloads/Images",
    ".png": "DESIGN", ".jpg": "DESIGN", ".jpeg": "DESIGN", ".svg": "DESIGN", ".gif": "DESIGN",

    # 4. Documents & Data
    "DOCUMENTS": r"/mnt/c/Users/Admin/Desktop/Downloads/Files",
    ".pdf": "DOCUMENTS", ".txt": "DOCUMENTS", ".md": "DOCUMENTS", ".csv": "DOCUMENTS", ".xlsx": "DOCUMENTS",

    # 5. Videos & Executables
    "MEDIA_APPS": r"/mnt/c/Users/Admin/Desktop/Downloads/Media_and_Apps",
    ".mp4": "MEDIA_APPS", ".mkv": "MEDIA_APPS", ".exe": "MEDIA_APPS", ".msi": "MEDIA_APPS",
}

EXTRACT_PATH = r"/mnt/c/Users/Admin/Desktop/Downloads/Extracted_Projects"

# ... (rest of the class logic remains exactly the same) ...

if __name__ == "__main__":
    # Extra check for WSL: Make sure the path actually exists in the Linux mount
    if not os.path.exists(WATCH_PATH):
        print(f"❌ ERROR: The path {WATCH_PATH} was not found. Check your Windows username.")
        exit(1)

    # Automatically create subfolders if they don't exist
    for key, path in DESTINATIONS.items():
        if key.isupper() and not os.path.exists(path):
            os.makedirs(path)
    if not os.path.exists(EXTRACT_PATH):
        os.makedirs(EXTRACT_PATH)

    observer = Observer()
    event_handler = AutomationHandler() # Ensure this class name matches your script
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"🛡️ Kahan's Sentinel is Active (WSL Mode) on: {WATCH_PATH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()