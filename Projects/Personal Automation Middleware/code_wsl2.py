import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- WSL CONFIGURATION ---
WATCH_PATH = r"/mnt/c/Users/Admin/Desktop/Downloads"

DESTINATIONS = {
    "CODING": os.path.join(WATCH_PATH, "Code"),
    "MUSIC": os.path.join(WATCH_PATH, "Music_Production"),
    "DESIGN": os.path.join(WATCH_PATH, "Images"),
    "DOCUMENTS": os.path.join(WATCH_PATH, "Files"),
    "MEDIA_APPS": os.path.join(WATCH_PATH, "Media_and_Apps"),
}

EXTRACT_PATH = os.path.join(WATCH_PATH, "Extracted_Projects")

# This name MUST match the one used in the 'if __name__' block below
class AutomationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)
        
        # Prevent infinite loops in the same folder
        if any(folder in file_path for folder in ["Code", "Music", "Images", "Files", "Media", "Extracted"]):
            return

        extension = os.path.splitext(file_name)[1].lower()
        if extension in ['.tmp', '.crdownload', '.part']:
            return

        time.sleep(2)

        if extension in ['.zip', '.rar', '.7z']:
            self.handle_zip(file_path, file_name)
        elif extension in DESTINATIONS:
            dest_folder = DESTINATIONS[DESTINATIONS[extension]]
            self.move_file(file_path, dest_folder, file_name)

    def handle_zip(self, source, name):
        try:
            extract_to = os.path.join(EXTRACT_PATH, os.path.splitext(name)[0])
            if not os.path.exists(extract_to): os.makedirs(extract_to)
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            os.remove(source)
            print(f"📦 Extracted: {name}")
        except Exception as e:
            print(f"❌ Zip Error: {e}")

    def move_file(self, source, dest, name):
        try:
            if not os.path.exists(dest): os.makedirs(dest)
            target = os.path.join(dest, name)
            if os.path.exists(target):
                name = f"{int(time.time())}_{name}"
                target = os.path.join(dest, name)
            shutil.move(source, target)
            print(f"🚀 Moved: {name}")
        except Exception as e:
            print(f"❌ Move Error: {e}")

if __name__ == "__main__":
    # Check if WSL path exists
    if not os.path.exists(WATCH_PATH):
        print(f"⚠️ Path not found: {WATCH_PATH}")
        exit()

    observer = Observer()
    # Ensure this variable name matches the CLASS name above
    event_handler = AutomationHandler() 
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"🤖 Kahan's Sentinel Active on WSL: {WATCH_PATH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()