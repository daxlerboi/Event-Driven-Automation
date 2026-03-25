import subprocess
import time
import threading
from queue import Queue
import sys
import os


class ChromeAutomation:
    def __init__(self):
        self.chrome_paths = self._get_chrome_path()
        self.event_queue = Queue()
        self.windows = []

    def _get_chrome_path(self):
        """Get Chrome executable path based on OS"""
        if sys.platform == "win32":
            return [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        elif sys.platform == "darwin":  # macOS
            return ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
        else:  # Linux
            return ["google-chrome", "google-chrome-stable", "chromium-browser"]

    def _find_chrome(self):
        """Find Chrome executable"""
        for path in self.chrome_paths:
            if os.path.exists(path) or subprocess.call(['which', path], stdout=subprocess.DEVNULL,
                                                       stderr=subprocess.DEVNULL) == 0:
                return path
        return None

    def open_chrome_window(self, url, window_name, user_data_dir=None):
        """Open a Chrome window with specified URL"""
        chrome_path = self._find_chrome()
        if not chrome_path:
            print("Chrome not found! Please install Google Chrome.")
            return None

        # Create a unique user data directory for each window to keep them separate
        if user_data_dir is None:
            user_data_dir = f"chrome_profile_{window_name}_{int(time.time())}"

        cmd = [
            chrome_path,
            f"--user-data-dir={user_data_dir}",
            "--new-window",
            url
        ]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Opened {window_name}: {url}")
            return {"process": process, "name": window_name, "url": url}
        except Exception as e:
            print(f"Error opening {window_name}: {e}")
            return None

    def close_all_windows(self):
        """Close all opened Chrome windows"""
        for window in self.windows:
            try:
                window["process"].terminate()
                print(f"Closed {window['name']}")
            except:
                pass
        self.windows.clear()

    def event_handler(self):
        """Event handler to process events from queue"""
        while True:
            try:
                event = self.event_queue.get(timeout=1)
                if event["type"] == "open":
                    window = self.open_chrome_window(event["url"], event["name"])
                    if window:
                        self.windows.append(window)
                elif event["type"] == "close":
                    self.close_all_windows()
                elif event["type"] == "exit":
                    break
            except:
                continue

    def trigger_open_event(self, url, name):
        """Trigger an open event"""
        self.event_queue.put({"type": "open", "url": url, "name": name})

    def trigger_close_event(self):
        """Trigger a close event"""
        self.event_queue.put({"type": "close"})

    def run(self, urls):
        """Run the automation with the provided URLs"""
        # Start event handler in background
        event_thread = threading.Thread(target=self.event_handler, daemon=True)
        event_thread.start()

        print("Event-driven Chrome automation started...")
        print("Opening windows...")

        # Trigger open events for each URL
        for i, (name, url) in enumerate(urls):
            self.trigger_open_event(url, name)
            time.sleep(2)  # Small delay between openings

        print("\nAll windows opened!")
        print("Press Enter to close all windows and exit...")
        input()

        # Trigger close event
        self.trigger_close_event()
        time.sleep(1)
        self.event_queue.put({"type": "exit"})

        print("Automation completed!")


def main():
    # Define the windows to open
    # Format: (window_name, url)
    windows_to_open = [
        ("YouTube", "https://www.youtube.com"),
        ("Google", "https://www.google.com"),
        ("GitHub", "https://github.com")
    ]

    # You can customize these URLs as needed
    # Example with different sites:
    # windows_to_open = [
    #     ("YouTube", "https://www.youtube.com"),
    #     ("News", "https://news.ycombinator.com"),
    #     ("Work", "https://mail.google.com")
    # ]

    # Create automation instance and run
    automation = ChromeAutomation()

    try:
        automation.run(windows_to_open)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Closing windows...")
        automation.close_all_windows()
        sys.exit(0)


if __name__ == "__main__":
    main()