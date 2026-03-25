Perfect! If all your `.txt` files are in

```
C:\Users\Admin\Desktop\Event-Driven Automation\Projects\Text2Markdown
```

and you want the `.md` files to be saved **in the same folder**, the **current setup already does this by default**.

Here’s how to use it step by step:

---

## 1️⃣ Open a command prompt

Press `Win + R`, type `cmd`, and hit Enter.

---

## 2️⃣ Navigate to your folder

```bat
cd "C:\Users\Admin\Desktop\Event-Driven Automation\Projects\Text2Markdown"
```

* Make sure `main.py` and the `converter` folder are inside this directory.

---

## 3️⃣ Convert a single file

```bat
python main.py example.txt
```

* `example.txt` is your input file.
* The script will automatically create `example.md` **in the same folder**.

---

## 4️⃣ Optional: Specify the output file name (still in the same folder)

```bat
python main.py example.txt example_converted.md
```

* This will save the converted Markdown file as `example_converted.md` in the same folder.

---

### ✅ Summary

* **Input location:** same folder (`Text2Markdown`)
* **Output location:** same folder (`Text2Markdown`)
* **No path changes needed** if you just want same-folder conversion.

---

If you want, I can **upgrade `main.py` to automatically convert all `.txt` files in that folder in one command**, so you don’t need to run it for each file manually.

Do you want me to do that?

