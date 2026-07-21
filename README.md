````md
# MP3 Cover & Metadata Editor

A simple desktop application built with **Python** and **Tkinter** that allows you to edit MP3 metadata in bulk without changing the original filenames.

## ✨ Features

- 🎵 Edit multiple MP3 files at once
- 🖼️ Replace album cover (JPG / PNG)
- 🎤 Change Artist
- 🎼 Change Track Title
- 💿 Change Album
- 📅 Change Year
- 📂 Original filenames remain unchanged
- 📊 Real-time progress bar
- 📝 Processing log
- 🖥️ Simple and user-friendly GUI

---

## 📸 Screenshot

> Add a screenshot of the application here.

```
assets/screenshot.png
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mp3-cover-editor.git

cd mp3-cover-editor
```

### 2. Install dependencies

```bash
pip install mutagen pillow
```

or

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

- Python 3.9+
- Tkinter (included with Python)
- Mutagen
- Pillow

Install manually:

```bash
pip install mutagen pillow
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

---

## 🛠 How to Use

### Step 1

Select one or more MP3 files.

### Step 2

(Optional)

Select a new cover image.

Supported formats:

- JPG
- JPEG
- PNG

### Step 3

(Optional)

Fill in any metadata you want to change:

- Artist
- Title
- Album
- Year

You can edit only the fields you need.

### Step 4

Click **Execute**.

The application will process every selected MP3 file.

---

## 📁 Supported Metadata

| Field | ID3 Tag |
|--------|----------|
| Cover | APIC |
| Artist | TPE1 |
| Title | TIT2 |
| Album | TALB |
| Year | TDRC |

---

## 📂 Project Structure

```
mp3-cover-editor/
│
├── main.py
├── README.md
├── requirements.txt
└── assets/
    └── screenshot.png
```

---

## 📚 Libraries Used

- Tkinter
- Mutagen
- Pillow
- pathlib
- threading
- os

---

## ⚙️ Technologies

- Python
- Tkinter GUI
- ID3 Metadata
- Multithreading

---

## ✅ Features Overview

- Bulk editing
- Cover replacement
- Metadata editing
- Progress tracking
- Error handling
- Log output
- Keeps original filenames
- Easy-to-use interface

---

## 📌 Notes

- Existing cover artwork will be replaced.
- Metadata fields left empty will remain unchanged.
- Original MP3 filenames are never modified.

---

## ❤️ Contributing

Pull requests are welcome.

If you have ideas for improvements, feel free to open an issue or submit a pull request.

---

## 📄 License

This project is released under the MIT License.

---

## 👨‍💻 Author

Developed with Python for easy bulk editing of MP3 covers and metadata.Eldos Erzhanuly
````
