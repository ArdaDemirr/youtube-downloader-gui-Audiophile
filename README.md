# audiophile

🎵 Audiophile
The Intelligent YouTube Downloader & Tagger

Audiophile is a modern, high-performance desktop application built with Python. Unlike standard downloaders, Audiophile focuses on music quality and organization. It doesn't just download files; it listens to them (via Shazam), identifies the official track details, and embeds studio-quality metadata directly into your MP3s.

✨ Key Features
🎧 Intelligent Metadata Tagging: Uses ShazamIO to audio-fingerprint every download. It automatically fixes:

Official Song Titles (Removing "Official Video", "Lyrics", etc.)

Artist, Album, & Year

Genre & Record Label

High-Res Cover Art (Embedded into the file)

📂 Clean Organization: Automatically renames files to a clean Artist - Title.mp3 format.

🚀 Smart History System: Tracks downloads by Video ID, not filename. You can rename or move your files, and Audiophile will still know you've already downloaded them (preventing duplicates).

⚡ Speed Boost: Uses concurrent fragment downloading to maximize bandwidth.

playlist Support: Download full playlists or select specific intervals (e.g., Songs 10-20).

🛑 Queue Management: Cancel downloads gracefully at any time.

🛠️ Installation

1. Prerequisites
   You need Python installed. You also need FFmpeg for media conversion.

2. Clone the Repository
   Bash
   git clone https://github.com/ArdaDemir/Audiophile.git
   cd Audiophile
3. Install Dependencies
   Bash
   pip install -r requirements.txt
4. Install FFmpeg (Important!)
   Because FFmpeg is too large to host on GitHub, you must add it manually:

Download ffmpeg-release-essentials.zip from gyan.dev.

Extract the zip file.

Copy ffmpeg.exe and ffprobe.exe (found in the bin folder).

Paste them into the main Audiophile folder (next to Audiophile.py).

🚀 Usage
Run the application:

Bash
python Audiophile.py
Paste a Link (YouTube Video/Playlist) OR type a Search Term.

Select Format (MP3 for audio, MP4 for video).

(Optional) Click ▼ Advanced:

Metadata: Turn on to auto-tag MP3s with official info and cover art.

Autocheck: Turn on to skip songs you have downloaded before.

Interval: Select a specific range of a playlist.

Hit Download.

🏗️ Built With
CustomTkinter: Modern UI library.

yt-dlp: The engine behind the downloads.

ShazamIO: Reverse audio engineering for metadata.

Mutagen: Industry-standard ID3 tagging.

⚠️ Disclaimer
This project is for educational purposes only. Please respect copyright laws and YouTube's Terms of Service. Do not download copyrighted content without permission.

Author: Arda Demir Build: V2.0 (Feb 2026)
