<div align="center">

<img src="icon.ico" width="80" alt="Audiophile Icon"/>

# Audiophile

### The YouTube Downloader & Tagger

![Version](https://img.shields.io/badge/version-v2.1-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Build](https://img.shields.io/badge/build-May%202026-orange?style=flat-square)

</div>

---

## What is Audiophile?

Audiophile downloads your audio, audio-fingerprints it through Shazam, and embeds the official studio metadata — title, artist, album, year, genre, record label, and high-resolution cover art — directly into the file. The result is a clean, properly tagged MP3 that looks native in any music player.

---

## Features

### Shazam-Powered Auto-Tagging

Every downloaded track is identified via ShazamIO audio fingerprinting. Audiophile automatically embeds:

- **Clean title** — strips "Official Video", "Lyrics", "(ft. ...)", etc.
- **Artist, Album & Year**
- **Genre & Record Label**
- **ISRC** — the unique international song identifier
- **Shazam link** — embedded as a web URL tag in the file
- **High-resolution cover art** — fetched and embedded directly into the MP3

### Smart File Organization

Files are automatically renamed to `Artist - Title.mp3` format. The raw Shazam JSON is saved alongside in a `metadata/` subfolder, also renamed to match.

### Smart History (Duplicate Prevention)

History is tracked by **YouTube Video ID**, not filename. You can rename, move, or reorganize your files — Audiophile still knows you've downloaded them. History is written per output folder in `download_history.txt`.

### Concurrent Fragment Downloading

Uses 8 parallel fragment downloads with 10MB chunk sizing to maximize your bandwidth, not just a single stream.

### Full Playlist Support

Download entire playlists or use interval selection to grab a specific range (e.g., songs 5–20 from a playlist).

### YouTube Search

No URL? Just type a search term. Audiophile will find and download the top result directly.

### Graceful Queue Management

The Download button becomes a **Stop Queue** button mid-download. Cancellation waits for the current file to finish cleanly — no corrupted files.

### Light & Dark Mode

Full theme support. Switch between modes live with a single button click.

---

## Installation

### Option A — Pre-built Executable (Recommended)

No Python or dependencies required. Just download and run.

1. Go to [**Releases**](https://github.com/ArdaDemirr/youtube-downloader-gui-Audiophile/releases)
2. Download `Audiophile.exe` from the latest release
3. Run it — that's it

> **Note:** Windows Defender or SmartScreen may flag the `.exe` as unknown on first run. This is expected for unsigned executables built with PyInstaller. Click **"More info → Run anyway"** to proceed.

---

### Option B — Run from Source

If you want to run or modify the Python source code directly.

#### 1. Prerequisites

- Python 3.10 or newer
- FFmpeg (required for source; **already bundled in the `.exe` release**)

#### 2. Clone the Repository

```bash
git clone https://github.com/ArdaDemirr/youtube-downloader-gui-Audiophile.git
cd youtube-downloader-gui-Audiophile
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install FFmpeg

FFmpeg is required when running from source. It is not included in the repository due to its size.

1. Download `ffmpeg-release-essentials.zip` from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the archive
3. Copy `ffmpeg.exe` and `ffprobe.exe` from the `bin/` folder
4. Paste them into the root project folder (next to `Audiophile.py`)

#### 5. Run

```bash
python Audiophile.py
```

---

## Usage

1. **Paste a link or type a search term** — YouTube video URL, playlist URL, or just keywords
2. **Select format** — MP3 for audio, MP4 for video
3. **Expand ▼ Advanced** (optional):

| Option        | What it does                                                         |
| ------------- | -------------------------------------------------------------------- |
| **metadata**  | Enables Shazam fingerprinting, full tag embedding, and file renaming |
| **autocheck** | Skips tracks already recorded in your download history               |
| **interval**  | Sets a start/end range for playlist downloads                        |

4. **Hit Download** — it becomes a **Stop Queue** button while active

---

## Output Structure

```
Your Output Folder/
├── Artist - Title.mp3          ← Renamed, fully tagged file
├── Artist - Title2.mp3
├── download_history.txt        ← Video IDs (for autocheck)
└── metadata/
    ├── Artist - Title.json     ← Raw Shazam response
    └── Artist - Title2.json
```

---

## Tech Stack

| Library                                                         | Role                            |
| --------------------------------------------------------------- | ------------------------------- |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)                      | Download engine                 |
| [ShazamIO](https://github.com/dotX12/ShazamIO)                  | Audio fingerprinting & metadata |
| [Mutagen](https://github.com/quodlibet/mutagen)                 | ID3 tag writing (MP3/ID3v2)     |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern GUI framework            |
| [Requests](https://docs.python-requests.org/)                   | Cover art fetching              |
| [FFmpeg](https://ffmpeg.org/)                                   | Audio conversion (source only)  |

---

## Changelog

### v2.1 — May 2026

- Redesigned control bar: Advanced options now collapse/expand in a unified panel
- ISRC tag embedding (`TSRC`) added to metadata pipeline
- Shazam URL embedded as `WXXX` web link tag
- Raw Shazam JSON automatically renamed to match the final MP3 filename
- YouTube search support — paste a search term instead of a URL
- Stop Queue button replaces Download mid-download; cancellation waits for current file to finish cleanly
- Concurrent fragment downloads increased to 8 with 10MB chunk sizing
- Window size locked to 500×500 min / 500×800 max for consistent layout
- Build: `24/05/2026`

### v2.0 — Feb 2026

- Initial public release
- Shazam metadata integration (title, artist, album, genre, cover art)
- Smart history tracking by YouTube Video ID
- Playlist interval selection
- Light / Dark theme toggle

---

## Disclaimer

This project is intended for educational and personal use only. Please respect copyright laws and [YouTube's Terms of Service](https://www.youtube.com/t/terms). Do not download content you do not have the right to download.

---

## Author

**Arda Demir**  
[GitHub @ArdaDemirr](https://github.com/ArdaDemirr)

---

<img width="622" height="666" alt="dark" src="https://github.com/user-attachments/assets/20af9d0a-7a6d-4b93-b572-e749390f7eaa" />

<img width="625" height="665" alt="light" src="https://github.com/user-attachments/assets/b9ff0ae6-9e24-4449-9638-590d44b9e4f2" />
