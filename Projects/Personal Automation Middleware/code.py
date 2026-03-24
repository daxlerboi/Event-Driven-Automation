import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# The folder the robot is watching
WATCH_PATH = r"C:\Users\Admin\Desktop\Downloads" 

# Define your "Buckets" - ALL located inside your Downloads folder
DESTINATIONS = {
    # 1. Coding & Development
    "CODING": r"C:\Users\Admin\Desktop\Downloads\Code",
    ".js": "CODING", ".jsx": "CODING", ".ts": "CODING", ".tsx": "CODING",
    ".py": "CODING", ".cpp": "CODING", ".c": "CODING", ".cs": "CODING",
    ".html": "CODING", ".css": "CODING", ".json": "CODING", ".env": "CODING",

    # 2. Audio & Music
    "MUSIC": r"C:\Users\Admin\Desktop\Downloads\Music_Production",
    ".wav": "MUSIC", ".mp3": "MUSIC", ".flac": "MUSIC", ".mid": "MUSIC", ".midi": "MUSIC",

    # 3. Images & Design
    "DESIGN": r"C:\Users\Admin\Desktop\Downloads\Images",
    ".png": "DESIGN", ".jpg": "DESIGN", ".jpeg": "DESIGN", ".svg": "DESIGN", ".gif": "DESIGN",

    # 4. Documents & Data
    "DOCUMENTS": r"C:\Users\Admin\Desktop\Downloads\Files",
    ".pdf": "DOCUMENTS", ".txt": "DOCUMENTS", ".md": "DOCUMENTS", ".csv": "DOCUMENTS", ".xlsx": "DOCUMENTS",

    # 5. Videos & Executables
    "MEDIA_APPS": r"C:\Users\Admin\Desktop\Downloads\Media_and_Apps",
    ".mp4": "MEDIA_APPS", ".mkv": "MEDIA_APPS", ".exe": "MEDIA_APPS", ".msi": "MEDIA_APPS",
}

# 6. Compressed (Auto-Extraction sub-folder)
EXTRACT_PATH = r"C:\Users\Admin\Desktop\Downloads\Extracted_Projects"

class AutomationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)
        
        # CRITICAL: If the file is already inside one of our sub-folders, IGNORE IT.
        # This prevents the script from trying to move a file it just moved.
        for key in ["Code", "Music_Production", "Images", "Files", "Media_and_Apps", "Extracted_Projects"]:
            if key in file_path:
                return

        extension = os.path.splitext(file_name)[1].lower()

        # Ignore temporary browser download files
        if extension in ['.tmp', '.crdownload', '.part']:
            return

        # Wait 2 seconds to ensure the download is actually finished
        time.sleep(2)

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
            # Create subfolder for this specific zip
            folder_name = os.path.splitext(name)[0]
            extract_to = os.path.join(EXTRACT_PATH, folder_name)
            
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
            
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            os.remove(source) 
            self.notify_dashboard(f"Extracted {name}")
        except Exception as e:
            print(f"Error unzipping {name}: {e}")

    def move_file(self, source, dest, name):
        try:
            if not os.path.exists(dest):
                os.makedirs(dest)
            
            # If a file with the same name exists, add a timestamp so we don't overwrite
            target_path = os.path.join(dest, name)
            if os.path.exists(target_path):
                name = f"{int(time.time())}_{name}"
                target_path = os.path.join(dest, name)

            shutil.move(source, target_path)
            print(f"🚀 Moved: {name} to {os.path.basename(dest)}")
            self.notify_dashboard(f"Moved {name} to {os.path.basename(dest)}")
        except Exception as e:
            print(f"Error moving {name}: {e}")

    def notify_dashboard(self, message):
        print(f"LOG: {message}")

if __name__ == "__main__":
    # Ensure all target folders exist
    for key, path in DESTINATIONS.items():
        if key.isupper() and not os.path.exists(path):
            os.makedirs(path)
    if not os.path.exists(EXTRACT_PATH):
        os.makedirs(EXTRACT_PATH)

    observer = Observer()
    event_handler = AutomationHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"🤖 Kahan's Robot is Watching: {WATCH_PATH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()