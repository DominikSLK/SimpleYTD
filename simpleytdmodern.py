# SimpleYTD by DominikSLK
from pathlib import Path
import time
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

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

a2 = "NO"
textclbef = ""
checked1 = "NO"
checked2 = "NO"
checked3 = "NO"

def on_closing():
    window.destroy()
    exit()

def download():  
    global a2
    global textclbef
    global checked1
    global checked2
    global checked3
    time.sleep(1)
    while True:
        textcl = clipboard.paste()
        if (textcl == textclbef):
            pass
        elif(textcl.find("youtube") != -1):
            entry_1.delete(0, tk.END)
            entry_1.insert(0, textcl)
            time.sleep(1)
            window.update()
            textclbef = textcl
        else:
            entry_1.delete(0, tk.END)
            textclbef = textcl
        if a2 == "YES":
            link = entry_1.get()

            if ((checked2 == "NO") and (checked3 == "NO")):
                if((link.find("youtube")) != -1 and (link.find("watch") != -1)):
                    yt = YouTube(link)
                    canvas.itemconfigure(entry_bg_1, image=entry_image_1_disabled)
                    entry_1.config(state='disabled')
                    clipboard.copy("")
                    canvas.itemconfigure(button1TXT, text="Downloading...")
                    window.update()

                    ys = yt.streams.get_highest_resolution()

                    videonameok = ys.default_filename.replace(".mp4", "")

                    ys.download()

                    if (checked1 == "YES"):
                        canvas.itemconfigure(button1TXT, text="Converting...")
                        window.update()
                        video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                        video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            if (checked2 == "YES"):
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

                        ys.download()

                        if (checked1 == "YES"):
                            canvas.itemconfigure(button1TXT, text="Converting...")
                            window.update()
                            video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            if (checked3 == "YES"):
                if(link.find("channel") != -1):
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

                        ys.download()
                        
                        videonameok = yt.title.replace(".", "").replace("|", "").replace("/", "").replace(":", "").replace(",", "")
                        if (checked1 == "YES"):
                            canvas.itemconfigure(button1TXT, text="Converting...")
                            window.update()
                            video = VideoFileClip(os.path.join("","",f"{videonameok}.mp4"))
                            video.audio.write_audiofile(os.path.join("","",f"{videonameok}.mp3"))

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

            canvas.itemconfigure(entry_bg_1, image=entry_image_1)
            entry_1.config(state='normal')
            a2 = "NO"

def download1(a):
    global a2
    canvas.itemconfigure(button1, image=buttonimageactive)
    window.update()
    time.sleep(0.1)
    canvas.itemconfigure(button1, image=buttonimage)
    a2 = "YES"

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

a = threading.Thread(target=download, daemon = True)
a.start()

window = tk.Tk()

window.geometry("714x350")
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

button1height = 160
button1text = "Download"

button1 = canvas.create_image(357,button1height, image=buttonimage, anchor='c')
button1TXT = canvas.create_text(357,button1height, text=button1text, font=("Sans Serif", 14))
canvas.tag_bind(button1, "<Button-1>", download1)
canvas.tag_bind(button1TXT, "<Button-1>", download1)

# check images
checkimage = PhotoImage(
    file=relative_to_assets("check.png"))
checkedimage = PhotoImage(
    file=relative_to_assets("checked.png"))

# check 1 begin
checked1 = "NO"
check1height = 210

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
check2height = 250

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
check3height = 290

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
