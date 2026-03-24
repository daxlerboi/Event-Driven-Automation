import os
import time
import shutil
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
WATCH_PATH = r"C:\Users\Admin\Desktop\Downloads"

DEST_CONFIG = {
    "CODING": ["Code", [".js", ".jsx", ".ts", ".tsx", ".py", ".cpp", ".c", ".cs", ".html", ".css", ".json", ".env"]],
    "MUSIC": ["Music_Production", [".wav", ".mp3", ".flac", ".mid", ".midi"]],
    "DESIGN": ["DESIGN", [".png", ".jpg", ".jpeg", ".svg", ".gif"]],
    "DOCUMENTS": ["Files", [".pdf", ".txt", ".md", ".csv", ".xlsx"]],
    "MEDIA_APPS": ["Media_and_Apps", [".mp4", ".mkv", ".exe", ".msi"]],
}

EXTRACT_PATH = os.path.join(WATCH_PATH, "Extracted_Projects")

class AutomationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Optional: Catch generic modifications if needed
        pass

    def on_created(self, event):
        if not event.is_directory:
            self.process_logic(event.src_path)

    def on_moved(self, event):
        # CRITICAL: This catches Chrome renaming ".crdownload" to ".jpg"
        if not event.is_directory:
            print(f"🔄 Rename detected: {os.path.basename(event.dest_path)}")
            self.process_logic(event.dest_path)

    def process_logic(self, file_path):
        file_name = os.path.basename(file_path)
        parent_folder = os.path.dirname(file_path)

        # 1. Strict Path Check (Only process files in the ROOT of Downloads)
        if parent_folder.lower() != WATCH_PATH.lower():
            return

        extension = os.path.splitext(file_name)[1].lower()

        # 2. Skip temp files immediately
        if extension in ['.tmp', '.crdownload', '.part', ''] or file_name.startswith('~'):
            return

        print(f"🔎 Analyzing: {file_name}")
        
        # 3. Wait for Chrome to release the file lock
        time.sleep(2) 

        # 4. Handle Zip Files
        if extension in ['.zip', '.rar', '.7z']:
            self.handle_zip(file_path, file_name)
            return

        # 5. Handle Standard Sorting
        for key, config in DEST_CONFIG.items():
            folder_name, extensions = config
            if extension in extensions:
                dest_folder = os.path.join(WATCH_PATH, folder_name)
                self.move_file(file_path, dest_folder, file_name)
                return

    def handle_zip(self, source, name):
        try:
            extract_to = os.path.join(EXTRACT_PATH, os.path.splitext(name)[0])
            if not os.path.exists(extract_to): os.makedirs(extract_to)
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            os.remove(source)
            print(f"📦 Unzipped: {name}")
        except Exception as e:
            print(f"❌ Zip Error: {e}")

    def move_file(self, source, dest, name):
        for i in range(5): # 5 Retries for stubborn Chrome locks
            try:
                if not os.path.exists(dest): os.makedirs(dest)
                target = os.path.join(dest, name)
                
                # Prevent overwriting
                if os.path.exists(target):
                    name = f"{int(time.time())}_{name}"
                    target = os.path.join(dest, name)

                shutil.move(source, target)
                print(f"🚀 Moved: {name} -> {os.path.basename(dest)}")
                break
            except PermissionError:
                time.sleep(1) # Wait and try again
            except Exception as e:
                print(f"❌ Move Error: {e}")
                break

if __name__ == "__main__":
    # Setup folders
    for folder_info in DEST_CONFIG.values():
        path = os.path.join(WATCH_PATH, folder_info[0])
        if not os.path.exists(path): os.makedirs(path)
    if not os.path.exists(EXTRACT_PATH): os.makedirs(EXTRACT_PATH)

    observer = Observer()
    event_handler = AutomationHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f"🤖 Kahan's Sentinel is Active on: {WATCH_PATH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()