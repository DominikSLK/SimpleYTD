# SimpleYTD by DominikSLK
import tkinter as tk
import os
from moviepy.video.io.VideoFileClip import *
from pytube import YouTube, Playlist, Channel
from tkinter import *
import time
import re
import threading
import clipboard
import unicodedata

a2 = "NO"
textclbef = ""

def on_closing():
    exit()

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return value

def download():  
    global a2
    global textclbef
    time.sleep(1)
    while True:
        textcl = clipboard.paste()
        if (textcl == textclbef):
            pass
        elif(textcl.find("youtube") != -1):
            entry.delete(0, tk.END)
            entry.insert(0, textcl)
            time.sleep(1)
            window.update()
            textclbef = textcl
        else:
            entry.delete(0, tk.END)
            textclbef = textcl
        if a2 == "YES":
            link = entry.get()
            

            if ((var2.get() == 0) and (var3.get() == 0)):
                if((link.find("youtube")) != -1 and (link.find("watch") != -1)):
                    yt = YouTube(link)
                    entry.config(state='disabled')
                    clipboard.copy("")
                    button['text'] = "Downloading..."
                    window.update()

                    ys = yt.streams.get_highest_resolution()
                    ys.download()
                    
                    videonameok = slugify(yt.title)

                    #videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "").replace("'", "").replace('"', '')
                    if (var1.get() == 1):
                        button['text'] = "Converting..."
                        window.update()
                        video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                        video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            if (var2.get() == 1):
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
                        ys.download()
                        
                        videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "")
                        if (var1.get() == 1):
                            button['text'] = "Converting..."
                            window.update()
                            video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            if (var3.get() == 1):
                if(link.find("channel") != -1):
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
                        ys.download()
                        
                        videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "")
                        if (var1.get() == 1):
                            button['text'] = "Converting..."
                            window.update()
                            video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            entry.config(state='normal')
            a2 = "NO"

def download1():
    global a2
    a2 = "YES"

def c2():
    if (var3.get() == 1):
        c3.deselect()

def c3():
    if (var3.get() == 1):
        c2.deselect()

a = threading.Thread(target=download, daemon = True)
a.start()

window = tk.Tk()
window.title('Simple Youtube Downloader')
window.iconphoto(False, tk.PhotoImage(file='icon.png'))
window.protocol("WM_DELETE_WINDOW", on_closing)
label = tk.Label(text="Link")
entry = tk.Entry(width=95)
label.pack()
entry.pack()
window.geometry("600x160")
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
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Convert to mp3?',variable=var1, onvalue=1, offvalue=0)
c1.pack()
c2 = tk.Checkbutton(window, text='Playlist?',variable=var2, onvalue=1, offvalue=0, command=c2)
c2.pack()
c3 = tk.Checkbutton(window, text='Channel?',variable=var3, onvalue=1, offvalue=0, command=c3)
c3.pack()
window.mainloop()
