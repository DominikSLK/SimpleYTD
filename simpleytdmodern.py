# SimpleYTD by DominikSLK
# -*- coding: utf-8 -*-
from pathlib import Path
import time
import tkinter as tk
import os
from moviepy.video.io.VideoFileClip import *
from pytubefix import YouTube, Playlist, Channel
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
checked1 = "NO"
checked2 = "NO"
checked3 = "NO"

def on_closing():
    window.destroy()
    exit()

def download():  
    global a2
    global a3
    global textclbef
    global checked1
    global checked2
    global checked3
    time.sleep(1)
    while True:
        if a2 == "YES":
            link = entry_1.get()

            if ((checked2 == "NO") and (checked3 == "NO") and (a3 != "YES") and (a3 != "YES")):
                if((link.find("youtube")) != -1 and (link.find("watch") != -1)):
                    yt = YouTube(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    canvas.itemconfigure(button1TXT, text="Downloading...")
                    window.update()

                    ys = yt.streams.get_highest_resolution()

                    videonameok = ys.default_filename.replace(".mp4", "")

                    ys.download(folderpath)

                    if (checked1 == "YES"):
                        canvas.itemconfigure(button1TXT, text="Converting...")
                        window.update()
                        video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                        video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"), logger=None)

                    canvas.itemconfigure(button1TXT, text="Download")
                    window.update()
                    entry_1.delete(0, tk.END)

                    canvas.itemconfigure(entrylabel, text="Downloaded as " + videonameok + ".mp4")
                    window.update() 
                    time.sleep(1)
                    if (checked1 == "YES"):
                        canvas.itemconfigure(entrylabel, text="Converted as " + videonameok + ".mp3")
                        window.update() 
                        time.sleep(1)
                    window.update() 
                    canvas.itemconfigure(entrylabel, text="Link")
                else:
                    canvas.itemconfigure(entrylabel, text="Not a video!", fill="red")
                    window.update()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link", fill="black")
                    window.update()

            if ((checked2 == "YES") and (a3 != "YES")):
                if(link.find("list") != -1):
                    canvas.itemconfigure(button1TXT, text="Downloading...")
                    window.update()
                    playlist = Playlist(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in playlist: %s' % len(playlist.video_urls))
                    canvas.itemconfigure(entrylabel, text='Number of videos in playlist: %s' % len(playlist.video_urls))
                    window.update() 
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
                    window.update() 
                    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(playlist.video_urls))

                    for url in playlist.video_urls:
                        yt = YouTube(url)
                        canvas.itemconfigure(button1TXT, text="Downloading...")
                        window.update()

                        ys = yt.streams.get_highest_resolution()

                        videonameok = ys.default_filename.replace(".mp4", "")

                        ys.download(folderpath)

                        if (checked1 == "YES"):
                            canvas.itemconfigure(button1TXT, text="Converting...")
                            window.update()
                            video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"), logger=None)

                        canvas.itemconfigure(button1TXT, text="Download")
                        window.update()
                        entry_1.delete(0, tk.END)

                        canvas.itemconfigure(entrylabel, text="Downloaded as " + videonameok + ".mp4")
                        window.update() 
                        time.sleep(1)
                        if (checked1 == "YES"):
                            canvas.itemconfigure(entrylabel, text="Converted as " + videonameok + ".mp3")
                            window.update() 
                            time.sleep(1)
                        window.update() 
                        canvas.itemconfigure(entrylabel, text="Link")
                else:
                    canvas.itemconfigure(entrylabel, text="Not a playlist!", fill="red")
                    canvas.itemconfigure(check2, image=checkimage)
                    window.update()
                    time.sleep(0.1)
                    checked2 = "NO"
                    window.update()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link", fill="black")
                    window.update()
            elif ((checked2 == "YES") and (a3 == "YES")):
                if(link.find("list") != -1):
                    canvas.itemconfigure(button3TXT, text="Getting list of videos...")
                    window.update()
                    playlist = Playlist(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in playlist: %s' % len(playlist.video_urls))
                    canvas.itemconfigure(entrylabel, text='Number of videos in playlist: %s' % len(playlist.video_urls))
                    window.update() 
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
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

                    canvas.itemconfigure(button3TXT, text="Get list of videos")
                    window.update()
                    entry_1.delete(0, tk.END)

                    canvas.itemconfigure(entrylabel, text="Created list of playlist " + playlist.title)
                    window.update() 
                    list.close()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
                else:
                    canvas.itemconfigure(entrylabel, text="Not a playlist!", fill="red")
                    canvas.itemconfigure(check2, image=checkimage)
                    window.update()
                    time.sleep(0.1)
                    checked2 = "NO"
                    window.update()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link", fill="black")
                    window.update()

            if ((checked3 == "YES") and (a3 != "YES")):
                if (link.find("/c") != -1) or (link.find("/@") != -1):
                    canvas.itemconfigure(button1TXT, text="Downloading...")
                    window.update()
                    channel = Channel(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    window.update() 
                    print('Number of videos in channel: %s' % len(channel.video_urls))
                    canvas.itemconfigure(entrylabel, text='Number of videos in channel: %s' % len(channel.video_urls))
                    window.update() 
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
                    window.update() 
                    channel._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(len(channel.video_urls))

                    for url in channel.video_urls:
                        yt = YouTube(url)
                        canvas.itemconfigure(button1TXT, text="Downloading...")
                        window.update()

                        ys = yt.streams.get_highest_resolution()

                        videonameok = ys.default_filename.replace(".mp4", "")

                        ys.download(folderpath)
                        
                        videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "")
                        if (checked1 == "YES"):
                            canvas.itemconfigure(button1TXT, text="Converting...")
                            window.update()
                            video = VideoFileClip(os.path.join(folderpath,"",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join(folderpath,"",f"{videonameok}.mp3"), logger=None)

                        canvas.itemconfigure(button1TXT, text="Download")
                        window.update()
                        entry_1.delete(0, tk.END)

                        canvas.itemconfigure(entrylabel, text="Downloaded as " + videonameok + ".mp4")
                        window.update() 
                        time.sleep(1)
                        if (checked1 == "YES"):
                            canvas.itemconfigure(entrylabel, text="Converted as " + videonameok + ".mp3")
                            window.update() 
                            time.sleep(1)
                        window.update() 
                        canvas.itemconfigure(entrylabel, text="Link")
                else:
                    canvas.itemconfigure(entrylabel, text="Not a channel!", fill="red")
                    canvas.itemconfigure(check3, image=checkimage)
                    window.update()
                    time.sleep(0.1)
                    checked3 = "NO"
                    window.update()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link", fill="black")
                    window.update()
            elif ((checked3 == "YES") and (a3 == "YES")):
                if (link.find("/c") != -1) or (link.find("/@") != -1):
                    canvas.itemconfigure(button3TXT, text="Getting list of videos...")
                    window.update()
                    channel = Channel(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    print('Number of videos in channel: %s' % len(channel.video_urls))
                    canvas.itemconfigure(entrylabel, text='Number of videos in channel: %s' % len(channel.video_urls))
                    window.update() 
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
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

                    canvas.itemconfigure(button3TXT, text="Get list of videos")
                    window.update()
                    entry_1.delete(0, tk.END)

                    canvas.itemconfigure(entrylabel, text="Created list of channel " + channel.channel_name)
                    window.update() 
                    list.close()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link")
                else:
                    canvas.itemconfigure(entrylabel, text="Not a channel!", fill="red")
                    canvas.itemconfigure(check3, image=checkimage)
                    window.update()
                    time.sleep(0.1)
                    checked3 = "NO"
                    window.update()
                    time.sleep(1)
                    canvas.itemconfigure(entrylabel, text="Link", fill="black")
                    window.update()

            canvas.itemconfigure(entry_bg_1, image=entry_image_1)
            entry_1.config(state='normal')
            entry_1.delete(0, tk.END)
            a2 = "NO"
            a3 = "NO"

def download1(a):
    global a2
    canvas.itemconfigure(button1, image=buttonimageactive)
    window.update()
    time.sleep(0.1)
    canvas.itemconfigure(button1, image=buttonimage)
    a2 = "YES"

def download2(a):
    global a3
    global a2
    canvas.itemconfigure(button3, image=buttonimagelongactive)
    window.update()
    time.sleep(0.1)
    canvas.itemconfigure(button3, image=buttonlongimage)
    a2 = "YES"
    a3 = "YES"

def ucheck1(a):
    global checked1
    if checked1 == "NO":
        canvas.itemconfigure(check1, image=checkedimage)
        window.update()
        time.sleep(0.1)
        checked1 = "YES"
    else:
        canvas.itemconfigure(check1, image=checkimage)
        window.update()
        time.sleep(0.1)
        checked1 = "NO"

def ucheck2(a):
    global checked2
    global checked3
    if checked2 == "NO" and checked3 != "YES":
        canvas.itemconfigure(check2, image=checkedimage)
        window.update()
        time.sleep(0.1)
        checked2 = "YES"
    elif checked2 == "NO" and checked3 == "YES":
        canvas.itemconfigure(check2, image=checkedimage)
        window.update()
        time.sleep(0.1)
        checked2 = "YES"
        canvas.itemconfigure(check3, image=checkimage)
        window.update()
        time.sleep(0.1)
        checked3 = "NO"
    else:
        canvas.itemconfigure(check2, image=checkimage)
        window.update()
        time.sleep(0.1)
        checked2 = "NO"

def ucheck3(a):
    global checked2
    global checked3
    if checked3 == "NO" and checked2 != "YES":
        canvas.itemconfigure(check3, image=checkedimage)
        window.update()
        time.sleep(0.1)
        checked3 = "YES"
    elif checked3 == "NO" and checked2 == "YES":
        canvas.itemconfigure(check3, image=checkedimage)
        window.update()
        time.sleep(0.1)
        checked3 = "YES"
        canvas.itemconfigure(check2, image=checkimage)
        window.update()
        time.sleep(0.1)
        checked2 = "NO"
    else:
        canvas.itemconfigure(check3, image=checkimage)
        window.update()
        time.sleep(0.1)
        checked3 = "NO"

def selectfolder(a):
    global folderpath
    canvas.itemconfigure(button2, image=buttonimagelongactive)
    window.update()
    time.sleep(0.1)
    canvas.itemconfigure(button2, image=buttonlongimage)
    folderpath = filedialog.askdirectory()
    button1_ttp = CreateToolTip(canvas, button2, "Selected folder: " + folderpath)
    button1TXT_ttp = CreateToolTip(canvas, button2TXT, "Selected folder: " + folderpath)

class CreateToolTip(object):
    def __init__(self, canvas, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.canvas = canvas
        self.widget = widget
        self.text = text
        self.canvas.tag_bind(widget, "<Enter>", self.enter)
        self.canvas.tag_bind(widget, "<Leave>", self.leave)
        self.canvas.tag_bind(widget, "<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.canvas.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.canvas.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.canvas.bbox(self.widget, "insert")
        x += self.canvas.winfo_rootx() + 25
        y += self.canvas.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.canvas)

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
        entry_1.delete(0, tk.END)
        entry_1.insert(0, textcl)
        window.update()
    else:
        entry_1.delete(0, tk.END)

a = threading.Thread(target=download, daemon = True)
a.start()

window = tk.Tk()

window.geometry("714x414")
window.configure(bg = "#C4C4C4")
window.title('Simple YouTube Downloader')
window.iconphoto(False, tk.PhotoImage(file=relative_to_assets('icon.png')))
window.protocol("WM_DELETE_WINDOW", on_closing)

canvas = Canvas(
    window,
    bg = "#C4C4C4",
    height = 545,
    width = 714,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

canvas.create_text(
    714/2,
    40.0,
    text="Simple YouTube Downloader",
    fill="#000000",
    font=("Roboto", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_image_1_disabled = PhotoImage(
    file=relative_to_assets("entry_1_disabled.png"))
entry_bg_1 = canvas.create_image(
    357.0,
    100.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=100.0,
    y=100.0,
    width=510.0,
    height=20.0
)

canvas.tag_bind(entry_bg_1, "<Enter>", pastelink)

entrylabel = canvas.create_text(
    98.0,
    80.0,
    anchor="nw",
    text="Link",
    fill="#000000",
    font=("Sans Serif", -14)
)

buttonimage = PhotoImage(
    file=relative_to_assets("button.png"))
buttonimageactive = PhotoImage(
    file=relative_to_assets("buttonactive.png"))

buttonlongimage = PhotoImage(
    file=relative_to_assets("buttonlong.png"))
buttonimagelongactive = PhotoImage(
    file=relative_to_assets("buttonlongactive.png"))

button1height = 160
button1text = "Download"

button1 = canvas.create_image(357,button1height, image=buttonimage, anchor='c')
button1TXT = canvas.create_text(357,button1height, text=button1text, font=("Sans Serif", 14))
canvas.tag_bind(button1, "<Button-1>", download1)
canvas.tag_bind(button1TXT, "<Button-1>", download1)

button2height = 210
button2text = "Select Download Folder"

button2 = canvas.create_image(357,button2height, image=buttonlongimage, anchor='c')
button2TXT = canvas.create_text(357,button2height, text=button2text, font=("Sans Serif", 14))
canvas.tag_bind(button2, "<Button-1>", selectfolder)
canvas.tag_bind(button2TXT, "<Button-1>", selectfolder)

button3height = 260
button3text = "Get list of videos"

button3 = canvas.create_image(357,button3height, image=buttonlongimage, anchor='c')
button3TXT = canvas.create_text(357,button3height, text=button3text, font=("Sans Serif", 14))
canvas.tag_bind(button3, "<Button-1>", download2)
canvas.tag_bind(button3TXT, "<Button-1>", download2)

# check images
checkimage = PhotoImage(
    file=relative_to_assets("check.png"))
checkedimage = PhotoImage(
    file=relative_to_assets("checked.png"))

# check 1 begin
checked1 = "NO"
check1height = 310

check1text = "Convert to MP3?"

check1TXT = canvas.create_text(357, check1height, text=check1text, font=("Sans Serif", 14))

bounds = canvas.bbox(check1TXT)
check1width = bounds[2] - bounds[0]

check1 = canvas.create_image(357 - 20 - (check1width / 2), check1height, image=checkimage, anchor='c')

canvas.tag_bind(check1, "<Button-1>", ucheck1)
canvas.tag_bind(check1TXT, "<Button-1>", ucheck1)
# check 1 end

# check 2 begin
checked2 = "NO"
check2height = 350

check2text = "Playlist?"

check2TXT = canvas.create_text(357, check2height, text=check2text, font=("Sans Serif", 14))

bounds = canvas.bbox(check2TXT)
check2width = bounds[2] - bounds[0]

check2 = canvas.create_image(357 - 20 - (check2width / 2), check2height, image=checkimage, anchor='c')

canvas.tag_bind(check2, "<Button-1>", ucheck2)
canvas.tag_bind(check2TXT, "<Button-1>", ucheck2)
# check 2 end

# check 3 begin
checked3 = "NO"
check3height = 390

check3text = "Channel?"

check3TXT = canvas.create_text(357, check3height, text=check3text, font=("Sans Serif", 14))

bounds = canvas.bbox(check3TXT)
check3width = bounds[2] - bounds[0]

check3 = canvas.create_image(357 - 20 - (check3width / 2), check3height, image=checkimage, anchor='c')

canvas.tag_bind(check3, "<Button-1>", ucheck3)
canvas.tag_bind(check3TXT, "<Button-1>", ucheck3)
# check 3 end

window.resizable(False, False)
window.mainloop()
