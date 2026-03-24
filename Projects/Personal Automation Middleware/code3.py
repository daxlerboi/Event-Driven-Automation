import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- THE REAL PATH FIX ---
# This ignores the Desktop and goes straight to the System Downloads folder
WATCH_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

# Verification check
if not os.path.exists(WATCH_PATH):
    # Fallback if your system is weirdly configured
    WATCH_PATH = r"C:\Users\Admin\Downloads"

print(f"✅ Robot is now watching the OFFICIAL path: {WATCH_PATH}")

DEST_FOLDERS = {
    "CODING": [".js", ".jsx", ".ts", ".tsx", ".py", ".cpp", ".c", ".cs", ".html", ".css", ".json", ".env"],
    "MUSIC": [".wav", ".mp3", ".flac", ".mid", ".midi"],
    "DESIGN": [".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"],
    "DOCUMENTS": [".pdf", ".txt", ".md", ".csv", ".xlsx"],
    "MEDIA_APPS": [".mp4", ".mkv", ".exe", ".msi"],
}

# Rest of your code (AutomationHandler, move_file, etc.) stays the same...

EXTRACT_PATH = os.path.join(WATCH_PATH, "EXTRACTED_PROJECTS")

class AutomationHandler(FileSystemEventHandler):
    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        file_name = os.path.basename(file_path)
        parent_folder = os.path.dirname(file_path)

        # Check if the path actually matches what the OS sees
        if parent_folder.lower() != WATCH_PATH.lower():
            return

        extension = os.path.splitext(file_name)[1].lower()

        if extension in ['.tmp', '.crdownload', '.part', ''] or file_name.startswith('~'):
            return

        print(f"🔎 Detected file: {file_name}")
        time.sleep(3) # Wait for Chrome to finish

        if extension in ['.zip', '.rar', '.7z']:
            self.handle_zip(file_path, file_name)
            return

        for folder_name, extensions in DEST_FOLDERS.items():
            if extension in extensions:
                dest_path = os.path.join(WATCH_PATH, folder_name)
                self.move_file(file_path, dest_path, file_name)
                return

    def handle_zip(self, source, name):
        try:
            extract_to = os.path.join(EXTRACT_PATH, os.path.splitext(name)[0])
            if not os.path.exists(extract_to): os.makedirs(extract_to)
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            os.remove(source)
            print(f"📦 Extracted: {name}")
        except Exception as e: print(f"❌ Zip Error: {e}")

    def move_file(self, source, dest, name):
        for i in range(5):
            try:
                if not os.path.exists(dest): os.makedirs(dest)
                target = os.path.join(dest, name)
                if os.path.exists(target):
                    name = f"{int(time.time())}_{name}"
                    target = os.path.join(dest, name)
                shutil.move(source, target)
                print(f"🚀 SUCCESS: {name} -> {os.path.basename(dest)}")
                break
            except PermissionError:
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error: {e}")
                break

if __name__ == "__main__":
    # Ensure the folders exist
    for folder in DEST_FOLDERS.keys():
        os.makedirs(os.path.join(WATCH_PATH, folder), exist_ok=True)
    os.makedirs(EXTRACT_PATH, exist_ok=True)

    observer = Observer()
    handler = AutomationHandler()
    observer.schedule(handler, WATCH_PATH, recursive=False)
    
    print(f"🤖 Kahan's Sentinel is RUNNING.")
    print(f"📍 Watching this EXACT folder: {WATCH_PATH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()