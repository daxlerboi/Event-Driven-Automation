# Keeping Your Automation Script Alive

Whether the code stays active or needs to be restarted depends entirely on how you run it. Since this is a Python script, it behaves like any other program: if you "kill" the process, the automation stops.

Here is the breakdown of how to keep it alive.

---

## 1. The Default Behavior (Manual Run)

If you just open a terminal and type `python kahan_sentinel.py`:

- **Active:** Only as long as that terminal window is open.
- **Deactivated:** The moment you close the terminal or restart your computer.

**Verdict:** You have to run it every time you start your PC.

---

## 2. The "Background" Behavior (Pythonw)

If you rename the file to `.pyw` (e.g., `kahan_sentinel.pyw`) and double-click it:

- **Active:** It runs in the "Background." You won't see a terminal window, but the script is watching your files.
- **Deactivated:** Only when you restart your computer or kill the task in Task Manager.

**Verdict:** Better, but still requires one manual click after you turn on your PC.

---

## 3. The "Permanent" Behavior (Auto-Startup)

To make it truly "Always Activated" without ever thinking about it again, you must tell Windows to start it for you.

### How to set it and forget it:

1. Press `Win + R` on your keyboard.
2. Type `shell:startup` and hit Enter. A folder will open.
3. Right-click your `kahan_sentinel.py` (or `.pyw`) file and select **Create Shortcut**.
4. Drag that **Shortcut** into the Startup folder you just opened.

Now, the moment you log into Windows, your "Robot" wakes up and starts sorting. You never have to run it manually again.

---

## 🔍 How to check if it's "Actually" Running

Since background scripts are invisible, you can verify they are active using the Task Manager:

1. Press `Ctrl + Shift + Esc`.
2. Click **More Details** (if it's small).
3. Go to the **Details** tab.
4. Look for `python.exe` or `pythonw.exe`.

If you see it, the script is "listening" to your folders.  
If you don't see it, the robot is "asleep."

---

## ⚠️ A Note on Code Changes

Because the script loads your "Rules" (the `DESTINATIONS` dictionary) into memory when it starts:

- If you change the code (e.g., you add a new folder for `.mp4` files), the running background version **won't know**.
- You must **Restart it**: Kill the process in Task Manager and run it again to "refresh" the rules.