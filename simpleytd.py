# SimpleYTD by DominikSLK
# -*- coding: utf-8 -*-
from pathlib import Path
import tkinter as tk
import os
from moviepy.video.io.VideoFileClip import *
from pytube import YouTube, Playlist, Channel
from tkinter import *
import time
import re
import threading
import clipboard
from tkinter import filedialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

a2 = "NO"
a3 = "NO"
textclbef = ""
folderpath = ""

def on_closing():
    window.destroy()
    exit()

def download():  
    global a2
    global a3
    global textclbef
    global folderpath
    time.sleep(1)
    while True:
        if a2 == "YES":
            link = entry.get()
            

            if ((var2.get() == 0) and (var3.get() == 0) and (a3 != "YES")):
                if((link.find("youtube")) != -1 and (link.find("watch") != -1)):
                    yt = YouTube(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    button['text'] = "Downloading..."
                    window.update()

                    ys = yt.streams.get_highest_resolution()

                    videonameok = ys.default_filename.replace(".mp4", "")

                    ys.download(folderpath)

                    if (var1.get() == 1):
                        button['text'] = "Converting..."
                        window.update()
                        video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                        video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"))

                    button['text'] = "Download"
                    window.update()
                    entry.delete(0, tk.END)

                    label['text'] = "Downloaded as " + videonameok + ".mp4"
                    window.update() 
                    time.sleep(1)
                    if (var1.get() == 1):
                        label['text'] = "Converted as " + videonameok + ".mp3"
                        window.update() 
                        time.sleep(1)
                    window.update() 
                    label['text'] = "Link"
                else:
                    label.config(fg="red")
                    label['text'] = "Not a video!"
                    window.update()
                    time.sleep(1)
                    label.config(fg="black")
                    label['text'] = "Link"
                    window.update()

            if ((var2.get() == 1) and (a3 != "YES")):
                if(link.find("list") != -1):
                    button['text'] = "Downloading..."
                    window.update()
                    playlist = Playlist(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in playlist: %s' % len(playlist.video_urls))
                    label['text'] = 'Number of videos in playlist: %s' % len(playlist.video_urls)
                    window.update() 
                    time.sleep(1)
                    label['text'] = "Link"
                    window.update() 
                    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(playlist.video_urls))

                    for url in playlist.video_urls:
                        yt = YouTube(url)
                        button['text'] = "Downloading..."
                        window.update()

                        ys = yt.streams.get_highest_resolution()

                        videonameok = ys.default_filename.replace(".mp4", "")

                        ys.download(folderpath)

                        if (var1.get() == 1):
                            button['text'] = "Converting..."
                            window.update()
                            video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"))

                        button['text'] = "Download"
                        window.update()
                        entry.delete(0, tk.END)

                        label['text'] = "Downloaded as " + videonameok + ".mp4"
                        window.update() 
                        time.sleep(1)
                        if (var1.get() == 1):
                            label['text'] = "Converted as " + videonameok + ".mp3"
                            window.update() 
                            time.sleep(1)
                        window.update() 
                        label['text'] = "Link"
                else:
                    label.config(fg="red")
                    label['text'] = "Not a playlist!"
                    c2.deselect()
                    window.update()
                    time.sleep(1)
                    label.config(fg="black")
                    label['text'] = "Link"
                    window.update()
            elif ((var2.get() == 1) and (a3 == "YES")):
                if(link.find("list") != -1):
                    button3['text'] = "Getting list of videos..."
                    window.update()
                    playlist = Playlist(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in playlist: %s' % len(playlist.video_urls))
                    label['text'] = 'Number of videos in playlist: %s' % len(playlist.video_urls)
                    window.update() 
                    time.sleep(1)
                    label['text'] = "Link"
                    window.update() 
                    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(playlist.video_urls))

                    if folderpath == "":
                        list = open(playlist.title + ".txt", "w", encoding="utf-8")
                    else:
                        list = open(folderpath + "/" + playlist.title + ".txt", "w", encoding="utf-8")

                    for url in playlist.video_urls:
                        yt = YouTube(url)

                        ys = yt.streams.get_lowest_resolution()

                        list.write(ys.title + "\n")
                        list.write(url + "\n")

                    button3['text'] = "Get list of videos"
                    window.update()
                    entry.delete(0, tk.END)


                    label['text'] = "Created list of playlist " + playlist.title
                    window.update() 
                    list.close()
                    time.sleep(1)
                    label['text'] = "Link"
                else:
                    label.config(fg="red")
                    label['text'] = "Not a playlist!"
                    c2.deselect()
                    window.update()
                    time.sleep(1)
                    label.config(fg="black")
                    label['text'] = "Link"
                    window.update()

            if ((var3.get() == 1) and (a3 != "YES")):
                if(link.find("/c") != -1):
                    button['text'] = "Downloading..."
                    window.update()
                    channel = Channel(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    window.update() 
                    print('Number of videos in channel: %s' % len(channel.video_urls))
                    label['text'] = 'Number of videos in channel: %s' % len(channel.video_urls)
                    window.update() 
                    time.sleep(1)
                    label['text'] = "Link"
                    window.update() 
                    channel._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(channel.video_urls))

                    for url in channel.video_urls:
                        yt = YouTube(url)
                        button['text'] = "Downloading..."
                        window.update()

                        ys = yt.streams.get_highest_resolution()

                        videonameok = ys.default_filename.replace(".mp4", "")

                        ys.download(folderpath)
                        
                        videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "")
                        if (var1.get() == 1):
                            button['text'] = "Converting..."
                            window.update()
                            video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"))

                        button['text'] = "Download"
                        window.update()
                        entry.delete(0, tk.END)

                        label['text'] = "Downloaded as " + videonameok + ".mp4"
                        window.update() 
                        time.sleep(1)
                        if (var1.get() == 1):
                            label['text'] = "Converted as " + videonameok + ".mp3"
                            window.update() 
                            time.sleep(1)
                        window.update() 
                        label['text'] = "Link"
                else:
                    label.config(fg="red")
                    label['text'] = "Not a channel!"
                    c3.deselect()
                    window.update()
                    time.sleep(1)
                    label.config(fg="black")
                    label['text'] = "Link"
                    window.update()
            elif ((var3.get() == 1) and (a3 == "YES")):
                if(link.find("/c") != -1):
                    button3['text'] = "Getting list of videos..."
                    window.update()
                    channel = Channel(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in channel: %s' % len(channel.video_urls))
                    label['text'] = 'Number of videos in channel: %s' % len(channel.video_urls)
                    window.update() 
                    time.sleep(1)
                    label['text'] = "Link"
                    window.update() 
                    channel._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(channel.video_urls))

                    if folderpath == "":
                        list = open(channel.channel_name + ".txt", "w", encoding="utf-8")
                    else:
                        list = open(folderpath + "/" + channel.channel_name + ".txt", "w", encoding="utf-8")

                    for url in channel.video_urls:
                        yt = YouTube(url)

                        ys = yt.streams.get_lowest_resolution()

                        list.write(ys.title + "\n")
                        list.write(url + "\n")

                    button3['text'] = "Get list of videos"
                    window.update()
                    entry.delete(0, tk.END)


                    label['text'] = "Created list of channel " + channel.channel_name
                    window.update() 
                    list.close()
                    time.sleep(1)
                    label['text'] = "Link"
                else:
                    label.config(fg="red")
                    label['text'] = "Not a channel!"
                    c3.deselect()
                    window.update()
                    time.sleep(1)
                    label.config(fg="black")
                    label['text'] = "Link"
                    window.update()

            entry.config(state='normal')
            entry.delete(0, tk.END)
            a2 = "NO"
            a3 = "NO"

def download1():
    global a2
    a2 = "YES"

def download2():
    global a3
    global a2
    a2 = "YES"
    a3 = "YES"

def c2():
    c3.deselect()

def c3():
    c2.deselect()

def selectfolder():
    global folderpath
    folderpath = filedialog.askdirectory()
    button2_ttp = CreateToolTip(button2, "Selected folder: " + folderpath)

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.widget)

        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def pastelink(a):
    textcl = clipboard.paste()
    if(textcl.find("youtube") != -1):
        entry.delete(0, tk.END)
        entry.insert(0, textcl)
        window.update()
    else:
        entry.delete(0, tk.END)

a = threading.Thread(target=download, daemon = True)
a.start()

window = tk.Tk()
window.title('Simple YouTube Downloader')
window.iconphoto(False, tk.PhotoImage(file=relative_to_assets('icon.png')))
window.protocol("WM_DELETE_WINDOW", on_closing)
label = tk.Label(text="Link")
entry = tk.Entry(width=95)
label.pack()
entry.pack()
entry.bind("<Enter>", pastelink)
window.geometry("600x240")
name = entry.get()
button = tk.Button(
    text="Download",
    width=12,
    height=1,
    bg="grey",
    fg="white",
    command=download1
)
button.pack(pady=(10, 10))
button2 = tk.Button(
    text="Select Download Folder",
    width=19,
    height=1,
    bg="grey",
    fg="white",
    command=selectfolder
)
button2.pack(pady=(1, 10))
button3 = tk.Button(
    text="Get list of videos",
    width=19,
    height=1,
    bg="grey",
    fg="white",
    command=download2
)
button3.pack(pady=(1, 10))
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Convert to MP3?',variable=var1, onvalue=1, offvalue=0)
c1.pack()
c2 = tk.Checkbutton(window, text='Playlist?',variable=var2, onvalue=1, offvalue=0, command=c2)
c2.pack()
c3 = tk.Checkbutton(window, text='Channel?',variable=var3, onvalue=1, offvalue=0, command=c3)
c3.pack()

window.resizable(False, False)
window.mainloop()
