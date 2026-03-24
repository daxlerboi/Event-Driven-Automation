import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Change this to the folder you want to watch (e.g., your Downloads)
WATCH_PATH = r"C:\Users\Kahan\Downloads" 

# Define your "Buckets" and where they should go
DESTINATIONS = {
    # 1. Coding & Development
    "CODING": r"C:\Users\Kahan\Desktop\Projects\Code",
    ".js": "CODING", ".jsx": "CODING", ".ts": "CODING", ".tsx": "CODING",
    ".py": "CODING", ".cpp": "CODING", ".c": "CODING", ".cs": "CODING",
    ".html": "CODING", ".css": "CODING", ".json": "CODING", ".env": "CODING",

    # 2. Audio & Music
    "MUSIC": r"C:\Users\Kahan\Desktop\Projects\Music_Production",
    ".wav": "MUSIC", ".mp3": "MUSIC", ".flac": "MUSIC", ".mid": "MUSIC", ".midi": "MUSIC",

    # 3. Images & Design
    "DESIGN": r"C:\Users\Kahan\Desktop\Assets\Images",
    ".png": "DESIGN", ".jpg": "DESIGN", ".jpeg": "DESIGN", ".svg": "DESIGN", ".gif": "DESIGN",

    # 4. Documents & Data
    "DOCUMENTS": r"C:\Users\Kahan\Documents\Files",
    ".pdf": "DOCUMENTS", ".txt": "DOCUMENTS", ".md": "DOCUMENTS", ".csv": "DOCUMENTS", ".xlsx": "DOCUMENTS",

    # 5. Videos & Executables
    "MEDIA_APPS": r"C:\Users\Kahan\Desktop\Media_and_Apps",
    ".mp4": "MEDIA_APPS", ".mkv": "MEDIA_APPS", ".exe": "MEDIA_APPS", ".msi": "MEDIA_APPS",
}

# 6. Compressed (Handled separately for Auto-Extraction)
EXTRACT_PATH = r"C:\Users\Kahan\Desktop\Projects\Extracted_Projects"

class AutomationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1].lower()

        # Wait a second to ensure the file is fully downloaded/pasted
        time.sleep(1)

        # CASE A: Compressed Files (Auto-Unzip)
        if extension in ['.zip', '.rar', '.7z']:
            self.handle_zip(file_path, file_name)
        
        # CASE B: Standard Sorting
        elif extension in DESTINATIONS:
            dest_folder = DESTINATIONS[DESTINATIONS[extension]]
            self.move_file(file_path, dest_folder, file_name)

    def handle_zip(self, source, name):
        try:
            print(f"📦 Extracting: {name}...")
            # Create subfolder for this specific zip to avoid mess
            extract_to = os.path.join(EXTRACT_PATH, os.path.splitext(name)[0])
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
            
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            os.remove(source) # Delete the original zip after extraction
            self.notify_dashboard(f"Extracted {name}")
        except Exception as e:
            print(f"Error unzipping {name}: {e}")

    def move_file(self, source, dest, name):
        try:
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.move(source, os.path.join(dest, name))
            print(f"🚀 Moved: {name} to {dest}")
            self.notify_dashboard(f"Moved {name} to {os.path.basename(dest)}")
        except Exception as e:
            print(f"Error moving {name}: {e}")

    def notify_dashboard(self, message):
        # This is where your MERN integration happens!
        # You would use requests.post("http://localhost:5000/api/log", json={"msg": message})
        print(f"LOG: {message}")

if __name__ == "__main__":
    observer = Observer()
    event_handler = AutomationHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"🤖 Kahan's Automation Robot is Active on {WATCH_PATH}...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()