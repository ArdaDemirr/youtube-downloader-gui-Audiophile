# Author: Arda Demir
# Build Date: 08/02/2026

import customtkinter
from customtkinter import CTkToplevel
from PIL import Image
from tkinter import filedialog
import os
import sys
import threading
import asyncio
import json
import yt_dlp
from shazamio import Shazam
import time
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TDRC, APIC, TCON, TPUB, TSRC, WXXX, COMM
from mutagen.mp3 import MP3
import requests
import json

# --- Helper Functions ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- GUI Setup ---
app = customtkinter.CTk()
app.geometry("500x500")
app.minsize(500, 500)
app.maxsize(500,800)
app.title("Audiophile V2.0")

try:
    iconPath = resource_path('icon.ico')
    app.iconbitmap(iconPath)
    iconPathTitle = resource_path('icon_title.ico')
    icon_image = Image.open(iconPathTitle)
    icon = customtkinter.CTkImage(dark_image=icon_image, size=(32, 32))
except Exception:
    icon = None 

mode = "dark"
customtkinter.set_appearance_mode(mode)

# --- Global State Flags ---
is_downloading = False
should_cancel = False

# --- FRAMES ---
# Header
imageFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
imageFrame.pack(fill="x", padx=10, pady=5)

# Inputs
linkFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
linkFrame.pack(fill="x", padx=10, pady=(5, 0))

pathFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
pathFrame.pack(fill="x", padx=10, pady=5)

# THE NEW UNIFIED CONTROL BAR
# This holds Toggle, Format, Download AND the Hidden Options
mainControlFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
mainControlFrame.pack(fill="x", padx=10, pady=0)

# Progress
progressFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
progressFrame.pack(fill="x", padx=10, pady=10)

StatusFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")
StatusFrame.pack(fill="both", expand=True, padx=10, pady=(0, 10))


# --- HEADER CONTENT ---
imageFrame.grid_columnconfigure(0, weight=1) 
imageFrame.grid_columnconfigure(1, weight=0) 

icon_label = customtkinter.CTkLabel(imageFrame, image=icon, text="Audiophile",
                                    text_color="#ff8503", compound="left", padx=10,
                                    font=customtkinter.CTkFont(family="Bauhaus 93", size=24))
icon_label.grid(row=0, column=0, sticky="") 

def change_event():
    global mode
    if mode == "dark":
        customtkinter.set_appearance_mode("light")
        mode = "light"
        changeButton.configure(text="Dark")
    else:
        customtkinter.set_appearance_mode("dark")
        mode = "dark"
        changeButton.configure(text="Light")

changeButton = customtkinter.CTkButton(imageFrame, text="Light", command=change_event,
                                       border_color="#000000", fg_color="#ff8503",
                                       hover_color="#FFBF00", corner_radius=20, width=40, height=15,
                                       font=customtkinter.CTkFont(family="garamond", size=11, weight="bold"))
changeButton.grid(row=0, column=1, sticky="e")


# --- INPUTS CONTENT ---
linkEntry = customtkinter.CTkEntry(linkFrame, placeholder_text="Link of video or playlist...",
                                   text_color="#ff8503", font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
linkEntry.pack(fill="x", expand=True)

pathFrame.grid_columnconfigure(0, weight=1) 
pathFrame.grid_columnconfigure(1, weight=0) 

pathEntry = customtkinter.CTkEntry(pathFrame, placeholder_text="Path...",
                                   text_color="#ff8503", font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
pathEntry.insert(0, os.getcwd())
pathEntry.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=(0,10))

def path_event():
    path = filedialog.askdirectory()
    if path:
        pathEntry.delete(0, customtkinter.END)
        pathEntry.insert(0, path)

pathButton = customtkinter.CTkButton(pathFrame, text=" . . . ", command=path_event,
                                     border_color="#000000", fg_color="#ff8503", hover_color="#FFBF00",
                                     width=30, height=10, font=customtkinter.CTkFont(family="garamond", size=10, weight="bold"))
pathButton.grid(row=0, column=1, sticky="e", pady=(0,10))


# --- CONTROL BAR LAYOUT (The Upgrade) ---

# Grid Setup:
# Col 0: Advanced Toggle (Left)
# Col 1: Spacer (Spring)
# Col 2: Format Switch
# Col 3: Download Button
mainControlFrame.grid_columnconfigure(1, weight=1) 

# 1. The Toggle Button
def toggle_advanced():
    if advancedContainer.winfo_ismapped():
        advancedContainer.grid_remove() # Hide Row 1
        advancedButton.configure(text="▼ Advanced")
    else:
        advancedContainer.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10,0)) # Show Row 1
        advancedButton.configure(text="▲ Advanced")

advancedButton = customtkinter.CTkButton(mainControlFrame, text="▼ Advanced", command=toggle_advanced,
                                         fg_color="transparent", text_color="#ff8503", hover_color=("#303030", "#e0e0e0"),
                                         width=100, height=20, font=customtkinter.CTkFont(family="garamond", size=14, weight="bold"))
advancedButton.grid(row=0, column=0, padx=(0, 10), sticky="w")

# 2. Format Switch
formatSwtch = customtkinter.CTkSegmentedButton(mainControlFrame, values=["Mp3", "Mp4"],
                                               selected_color="#ff8503", selected_hover_color="#FFBF00",
                                               font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))

formatSwtch.set("Mp3")
formatSwtch.grid(row=0, column=1, padx=(40, 40), sticky="ew")

# 3. Download Button
downloadButton = customtkinter.CTkButton(mainControlFrame, text="Download", command=lambda: download_event(),
                                         fg_color="#ff8503", border_color="#000000", hover_color="#FFBF00",
                                         width=100, font=customtkinter.CTkFont(family="garamond", size=14, weight="bold"))
downloadButton.grid(row=0, column=2, padx=(10, 0), sticky="e")


# --- THE HIDDEN ROW (Row 1) ---
advancedContainer = customtkinter.CTkFrame(mainControlFrame, fg_color="transparent")
# Note: We do NOT grid it yet. The toggle button does that.

# Configure internal layout of the hidden row
advancedContainer.grid_columnconfigure(2, weight=0) # Spacer between metadata and interval

# AutoCheck
def autocheck_event():
    if autoCheckCheckbox.get() == 1:
        autoCheckCheckbox.configure(text="autocheck", text_color="#ff8503")
    else:
        autoCheckCheckbox.configure(text="autocheck?", text_color="dark grey")

autoCheck_var = customtkinter.BooleanVar(value=False)
autoCheckCheckbox = customtkinter.CTkCheckBox(advancedContainer, text="autocheck?", variable=autoCheck_var,
                                              command=autocheck_event, onvalue=True, offvalue=False,
                                              fg_color="#ff8503", hover_color="#FFBF00", text_color="dark grey",
                                              font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
autoCheckCheckbox.grid(row=0, column=0, sticky="", padx=(25, 25))

# Metadata
def metadata_event():
    if metadata_var.get() == 1:
        metadataCheckbox.configure(text="metadata", text_color="#ff8503")
    else:
        metadataCheckbox.configure(text="metadata?", text_color="dark grey")

metadata_var = customtkinter.BooleanVar(value=False)
metadataCheckbox = customtkinter.CTkCheckBox(advancedContainer, text="metadata?", variable=metadata_var,
                                             command=metadata_event, onvalue=True, offvalue=False,
                                             fg_color="#ff8503", hover_color="#FFBF00", text_color="dark grey",
                                             font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
metadataCheckbox.grid(row=0, column=1, sticky="")

# Interval
def select_event():
    if switch_var.get() == "on":
        videoNumberStart.grid(row=0, column=4, padx=(0,5))
        videoNumberEnd.grid(row=0, column=5, padx=(0,5))
        selectSwitch.configure(text="interval ", text_color="#ff8503")
    else:
        videoNumberStart.grid_forget()
        videoNumberEnd.grid_forget()
        selectSwitch.configure(text="interval? ", text_color="dark grey")

switch_var = customtkinter.StringVar(value="off")
selectSwitch = customtkinter.CTkSwitch(advancedContainer, text="interval? ", text_color="dark grey",
                                       command=select_event, variable=switch_var, onvalue="on", offvalue="off",
                                       progress_color="#ff8503", button_hover_color="#FFBF00",
                                       font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
selectSwitch.grid(row=0, column=2, sticky="", padx=(25,0))

videoNumberStart = customtkinter.CTkEntry(advancedContainer, width=50, height=20, placeholder_text="Start",
                                          text_color="#ff8503", font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
videoNumberEnd = customtkinter.CTkEntry(advancedContainer, width=50,height=20, placeholder_text="End",
                                        text_color="#ff8503", font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))


# --- PROGRESS ---
progressFrame.grid_columnconfigure(0, weight=1) 
progressFrame.grid_columnconfigure(1, weight=0) 

progressbar = customtkinter.CTkProgressBar(progressFrame, height=5, mode="determinate", progress_color="#ff8503")
progressbar.set(0)
progressbar.grid(row=0, column=0, sticky="ew", padx=(0, 10)) 

def clean_event():
    statusBox.configure(state="normal")
    statusBox.delete(0.0, customtkinter.END)
    statusBox.configure(state="disable")
    progressbar.set(0)

cleanButton = customtkinter.CTkButton(progressFrame, text="CLR", command=clean_event,
                                      fg_color="#ff8503", border_color="#000000", hover_color="#FFBF00",
                                      width=40, height=15, font=customtkinter.CTkFont(family="garamond", size=10, weight="bold"))
cleanButton.grid(row=0, column=1)


# --- LOGIC CORE ---

def log_message(message):
    def _update():
        statusBox.configure(state="normal")
        statusBox.insert("end", f"\n{message}")
        statusBox.see("end")
        statusBox.configure(state="disabled")
    app.after(0, _update)

def update_progress(val):
    app.after(0, lambda: progressbar.set(val))

async def process_metadata(file_path, save_dir):
    try:
        if not file_path or not os.path.exists(file_path): return
        
        # --- 1. SCAN (Shazam) ---
        shazam = Shazam()
        #log_message(f"Identifying: {os.path.basename(file_path)}...")
        out = await shazam.recognize_song(file_path)
        
        # --- 2. SAVE RAW JSON (Temporary Name) ---
        # We save it with the original filename first to ensure we have the data
        meta_dir = os.path.join(save_dir, "metadata")
        os.makedirs(meta_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        original_json_path = os.path.join(meta_dir, f"{base_name}.json")
        
        with open(original_json_path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=4, ensure_ascii=False)
        #log_message(f"JSON Saved: {base_name}.json")

        # --- 3. EXTRACT ALL DATA ---
        track = out.get('track', {})
        if not track:
            log_message("No match found for tags.")
            return

        # Basic Info
        title = track.get('title')
        artist = track.get('subtitle')
        genre = track.get('genres', {}).get('primary')
        cover_url = track.get('images', {}).get('coverarthq')
        web_url = track.get('url') # Shazam Link
        isrc = track.get('isrc')   # Unique Song ID
        
        # Deep Dive for Album, Label, and Year
        album = "Unknown Album"
        label = None
        year = None
        
        for section in track.get('sections', []):
            if section.get('type') == 'SONG':
                for meta in section.get('metadata', []):
                    if meta['title'] == 'Album': album = meta['text']
                    if meta['title'] == 'Label': label = meta['text']
                    if meta['title'] == 'Released': year = meta['text']

        # --- 4. EMBED TAGS (Mutagen) ---
        try:
            audio = MP3(file_path, ID3=ID3)
            try: audio.add_tags()
            except: pass 

            # Standard Tags
            if title: audio.tags.add(TIT2(encoding=3, text=title))
            if artist: audio.tags.add(TPE1(encoding=3, text=artist))
            if album: audio.tags.add(TALB(encoding=3, text=album))
            if genre: audio.tags.add(TCON(encoding=3, text=genre))
            
            # Date/Year
            if year: 
                audio.tags.add(TYER(encoding=3, text=str(year)))
                audio.tags.add(TDRC(encoding=3, text=str(year)))

            # Extended Metadata
            if label: audio.tags.add(TPUB(encoding=3, text=label))
            if isrc:  audio.tags.add(TSRC(encoding=3, text=isrc))
            if web_url: audio.tags.add(WXXX(encoding=3, desc=u'Shazam', url=web_url))

            # Cover Art
            if cover_url:
                try:
                    img_data = requests.get(cover_url).content
                    audio.tags.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3, 
                        desc=u'Cover',
                        data=img_data
                    ))
                except Exception as e:
                    log_message(f"Art Error: {e}")
            
            audio.save()
            log_message(f"Metadata Completed: {base_name}")
            
        except Exception as e:
            log_message(f"Tagging Failed: {e}")

        # --- 5. RENAME BOTH FILES (Clean Name) ---
        if title and artist:
            # Sanitize filename
            clean_title = "".join([c for c in title if c not in '<>:"/\\|?*'])
            clean_artist = "".join([c for c in artist if c not in '<>:"/\\|?*'])
            
            new_base_name = f"{clean_artist} - {clean_title}"
            
            # A. Rename MP3
            new_mp3_path = os.path.join(save_dir, f"{new_base_name}.mp3")
            
            if not os.path.exists(new_mp3_path):
                try:
                    os.rename(file_path, new_mp3_path)
                    #log_message(f"Renamed MP3: {new_base_name}.mp3")
                except Exception as e:
                    log_message(f"MP3 Rename Failed: {e}")
            else:
                log_message(f"MP3 Rename skipped (File exists)")

            # B. Rename JSON (To match the new MP3 name)
            new_json_path = os.path.join(meta_dir, f"{new_base_name}.json")
            
            if os.path.exists(original_json_path) and not os.path.exists(new_json_path):
                try:
                    os.rename(original_json_path, new_json_path)
                    #log_message(f"Renamed JSON to match.")
                except Exception as e:
                    log_message(f"JSON Rename Failed: {e}")

    except Exception as e:
        log_message(f"Meta Process Error: {str(e)[:50]}...")

def run_download_process(link, path, fmt, use_metadata, auto_check, interval_on, start_idx, end_idx):
    global is_downloading, should_cancel
    
    try:
        if not os.path.exists(path): os.makedirs(path)
        
        ffmpeg_local = os.path.join(os.getcwd(), 'ffmpeg.exe')
        history_file = os.path.join(path, "download_history.txt") # The Manual History File
        
        base_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'ignoreerrors': True,
            'quiet': True,
            'noprogress': True,
            'concurrent_fragment_downloads': 5, # Speed Boost
            'http_chunk_size': 10485760,
        }

        if os.path.exists(ffmpeg_local):
            base_opts['ffmpeg_location'] = ffmpeg_local
        
        if fmt == "Mp3":
            base_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            })
        else:
            base_opts.update({'format': 'bestvideo+bestaudio/best'})

        # --- 1. LOAD HISTORY (Manual Check) ---
        downloaded_ids = set()
        if auto_check and os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    downloaded_ids = set(line.strip() for line in f if line.strip())
            except: pass

        # --- 2. DETECT MODE ---
        is_playlist_mode = "playlist" in link
        scanner_opts = base_opts.copy()
        
        # We handle history manually, so we don't use yt-dlp's internal archive
        if 'download_archive' in scanner_opts: del scanner_opts['download_archive']

        if is_playlist_mode:
            log_message("Scanning Playlist...")
            scanner_opts['extract_flat'] = 'in_playlist'
        else:
            log_message("Downloading Video...")
            scanner_opts['noplaylist'] = True 

        if should_cancel: raise Exception("Cancelled")

        entries_to_download = []

        with yt_dlp.YoutubeDL(scanner_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            
            if is_playlist_mode and 'entries' in info:
                all_entries = list(info['entries'])
                total_found = len(all_entries)
                log_message(f"Playlist Found: {total_found} videos.")
                
                if interval_on:
                    try:
                        s = int(start_idx) - 1 if start_idx else 0
                        e = int(end_idx) if end_idx else total_found
                        s = max(0, s); e = min(total_found, e)
                        entries_to_download = all_entries[s:e]
                        log_message(f"Interval Selected: {s+1} to {e}")
                    except ValueError:
                        entries_to_download = all_entries
                else:
                    entries_to_download = all_entries
            else:
                entries_to_download = [info]

        # --- 3. FILTER QUEUE (The Check) ---
        final_queue = []
        for entry in entries_to_download:
            vid_id = entry.get('id')
            title = entry.get('title', 'Unknown')
            
            # If AutoCheck is ON and ID is in history, skip completely
            if auto_check and vid_id and vid_id in downloaded_ids:
                log_message(f"Skipping (History): {title}")
                continue 
            
            final_queue.append(entry)

        # --- 4. DOWNLOAD LOOP ---
        total_tasks = len(final_queue)
        if total_tasks == 0 and len(entries_to_download) > 0:
            log_message("All items skipped (Already in history).")
        else:
            log_message(f"Downloading {total_tasks} new item(s)...\n--------------------------------------------------")

        dl_opts = base_opts.copy()
        
        # --- THE SPEED FIX ---
        # We force 'noplaylist' to True here because we are iterating 1-by-1.
        # This prevents yt-dlp from re-scanning the whole playlist for every song.
        dl_opts['noplaylist'] = True 

        for i, entry in enumerate(final_queue):
            if should_cancel: 
                log_message("Queue stopped.")
                break

            url = entry.get('url') or entry.get('webpage_url')
            vid_id = entry.get('id')
            title = entry.get('title', 'Unknown Video')
            
            if not url: continue
            
            if total_tasks > 0: update_progress((i + 1) / total_tasks)
            log_message(f"[{i+1}/{total_tasks}] Downloading: {title}")
            
            try:
                with yt_dlp.YoutubeDL(dl_opts) as ydl: 
                    ydl.download([url])
                
                # --- 5. UPDATE HISTORY (Immediate Save) ---
                if vid_id:
                    try:
                        with open(history_file, 'a', encoding='utf-8') as f:
                            f.write(f"{vid_id}\n")
                        downloaded_ids.add(vid_id) # Update memory set too
                    except: pass

            except Exception as e:
                log_message(f"Skipping {title}: {str(e)}")

        # --- 6. METADATA ---
        if use_metadata and fmt == "Mp3":
            log_message("--------------------------------------------------\nStarting Metadata Scan...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            meta_folder = os.path.join(path, "metadata")
            files_to_scan = []
            
            for f in os.listdir(path):
                if f.endswith(".mp3"):
                    # Only scan if JSON doesn't exist yet (prevents re-tagging renamed files)
                    base = os.path.splitext(f)[0]
                    json_p = os.path.join(meta_folder, f"{base}.json")
                    if not os.path.exists(json_p):
                        files_to_scan.append(os.path.join(path, f))

            if files_to_scan:
                count = len(files_to_scan)
                for idx, mp3 in enumerate(files_to_scan):
                    if should_cancel: break
                    log_message(f"Metadata [{idx+1}/{count}]...")
                    loop.run_until_complete(process_metadata(mp3, path))
            else:
                log_message("No new files to tag.")

            loop.close()

        if should_cancel:
            log_message("Stopped.")
        else:
            log_message("--------------------------------------------------\nAll Tasks Finished.")
            update_progress(1.0)

    except Exception as e:
        log_message(f"Status: {str(e)}")

    finally:
        is_downloading = False
        should_cancel = False
        app.after(0, lambda: downloadButton.configure(text="Download", state="normal", fg_color="#ff8503"))

def download_event():
    global is_downloading, should_cancel
    
    # 1. HANDLE CANCEL CLICK
    if is_downloading:
        should_cancel = True
        # Update text to inform user we are waiting for the current file
        downloadButton.configure(text="Finishing...", state="disabled") 
        return

    # 2. HANDLE DOWNLOAD CLICK
    link = linkEntry.get()
    path = pathEntry.get()
    fmt = formatSwtch.get()
    auto_check = autoCheck_var.get()
    use_metadata = metadata_var.get()
    interval_on = (switch_var.get() == "on")
    start = videoNumberStart.get()
    end = videoNumberEnd.get()

    if not link:
        log_message("Error: Link required.")
        return

    is_downloading = True
    should_cancel = False
    
    downloadButton.configure(text="Stop Queue", fg_color="#D22B2B") 
    clean_event()
    
    t = threading.Thread(target=run_download_process, args=(link, path, fmt, use_metadata, auto_check, interval_on, start, end))
    t.start()

statusBox = customtkinter.CTkTextbox(StatusFrame, text_color="#ff8503",
                                     font=customtkinter.CTkFont(family="garamond", size=13, weight="bold"))
statusBox.configure(state="disabled")
statusBox.pack(fill="both", expand=True, padx=0, pady=0)

app.mainloop()