# SimpleYTD v2 by DominikSLK
# -*- coding: utf-8 -*-
from pathlib import Path
import tkinter as tk
import os
from moviepy.video.io.VideoFileClip import *
from pytube import YouTube, Playlist, Channel
from tkinter import *
import time
import threading
import clipboard
from tkinter import filedialog
import customtkinter
import sys
from proglog import TqdmProgressBarLogger

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

get_list_of_videos = False

queue = {}
pb_labels = {}
progress_bars = {}
percent_labels = {}
pb_count = 0
adding_done = True

class ToolTip():
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

    def set_text(self, text):
        self.text = text

class PrintLogger():
    def __init__(self):
        pass

    def write(self, text):
        app.textbox.configure(state="normal")
        app.textbox.insert(tk.END, text)
        app.textbox.see("end")
        app.textbox.configure(state="disabled")

    def flush(self):
        app.textbox.configure(state="normal")
        app.textbox.insert(tk.END, "\n")
        app.textbox.see("end")
        app.textbox.configure(state="disabled")

class BarLogger(TqdmProgressBarLogger):
    def __init__(self, init_state=None, bars=None, leave_bars=False, ignored_bars=None, logged_bars='all', notebook='default', print_messages=True, min_time_interval=0, ignore_bars_under=0, videoname=""):
        super().__init__(init_state, bars, leave_bars, ignored_bars, logged_bars, notebook, print_messages, min_time_interval, ignore_bars_under)
        self.videoname = videoname
        self.total = 0
        self.before = 0

    def bars_callback(self, bar, attr, value, old_value):
        if attr == "total":
            self.total = value
        elif attr == "index":
            if (self.before >= 0.5) or (value == self.total):
                self.before = 0

                self.bar_update(value / self.total)
                percent = str(round((value / self.total) * 100, 1))
                percent_labels[self.videoname].configure(text=f"{percent}%")
            else:
                self.before += ((value / self.total) * 100) - (old_value / self.total) * 100

    def bar_update(self, value):
        progress_bars[self.videoname].set(value)

def progress_function(chunk, file_handle, bytes_remaining):
    current = ((chunk.filesize - bytes_remaining)/chunk.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress_bars[chunk.default_filename].set(current)
    if not percent == None:
        percent_labels[chunk.default_filename].configure(text=percent + "%")

def download_video(url):    
    global pb_count
    global progress_bars
    global adding_done

    yt = YouTube(url, on_progress_callback=progress_function)
    clipboard.copy("")

    ys = yt.streams.get_highest_resolution()

    queue[url] = ys.default_filename

    pb_label = customtkinter.CTkLabel(app.queue_frame, text=ys.default_filename, anchor="w")
    pb_label.grid(row=pb_count, column=0, padx=0, pady=0, columnspan=2)
    progressbar = customtkinter.CTkProgressBar(app.queue_frame)
    progressbar.grid(row=pb_count+1, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

    percent_label = customtkinter.CTkLabel(app.queue_frame, text="0%", anchor="n")
    percent_label.grid(row=pb_count+1, column=1, padx=0, pady=0)

    pb_count += 2

    progressbar.set(0)

    progress_bars[ys.default_filename] = progressbar
    percent_labels[ys.default_filename] = percent_label
    pb_labels[ys.default_filename] = pb_label

    adding_done = True

    app.update()

    ys.download(app.folderpath)

    if (app.convert_to_mp3.get() == 1):
        convert_to_mp3(ys.default_filename)

def convert_to_mp3(videoname):
    logger = BarLogger(videoname=videoname)

    videonameok = videoname.replace(".mp4", "")

    pb_labels[videoname].configure(text=f"{videonameok}.mp3")
    progress_bars[videoname].set(0)
    percent_labels[videoname].configure(text="0%")
    progress_bars[videoname].configure(progress_color="orange")
    video = VideoFileClip(os.path.join(app.folderpath,"", f"{videonameok}.mp4"))
    video.audio.write_audiofile(os.path.join(app.folderpath,"", f"{videonameok}.mp3"), logger=logger)

def download_work():
    global get_list_of_videos

    link = app.entry.get()

    # get list of videos
    if (((app.is_playlist.get() == 1) or (app.is_channel.get() == 1)) and (get_list_of_videos)):
        list_type = ""
        playlist = None
        list_name = ""

        if (link.find("list") != -1) or (link.find("/c") != -1) or (link.find("/@") != -1):

            #Check if channel or playlist
            if (link.find("list") != -1):
                playlist = Playlist(link)
                list_name = playlist.title
                list_type = "playlist"
            else:
                playlist = Channel(link)
                list_name = playlist.channel_name
                list_type = "channel"

            app.get_list_of_videos_btn.configure(text="Getting list of videos...")
            app.update()
            
            app.entry.configure(state='disabled')
            clipboard.copy("")
            msg = f'Number of videos in {list_type}: {len(playlist.video_urls)}'
            print(msg)
            app.label.configure(text=msg)
            app.update() 
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
            app.update()

            file_content = ""

            if app.folderpath == "":
                list = open(list_name + ".txt", "w", encoding="utf-8")
            else:
                list = open(app.folderpath + "/" + list_name + ".txt", "w", encoding="utf-8")

            for url in playlist.video_urls:
                yt = YouTube(url)

                try:
                    a = yt.title + "\n" + url + "\n"
                    file_content += a
                except:
                    ys = yt.streams.get_lowest_resolution()
                    a = ys.title + "\n" + url + "\n"
                    file_content += a
                    
                list.write(a)
                list.flush()
                
            list.close()

            app.get_list_of_videos_btn.configure(text="Get list of videos")
            app.update()
            app.entry.delete(0, tk.END)

            app.label.configure(text="Created list of channel " + list_name)
            app.update() 
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
        else:
            app.label.configure(text="Not a playlist or a channel!", text_color="red")
            app.is_channel.deselect()
            app.update()
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
            app.update()
            
    # normal video
    if ((app.is_playlist.get() == 0) and (app.is_channel.get() == 0) and (not get_list_of_videos)):
        if((link.find("youtube")) != -1 and (link.find("watch") != -1)):
            download_video(link)

            progress_bars[queue[link]].set(1)
            percent_labels[queue[link]].configure(text="100%")

            videonameok = queue[link].replace(".mp4", "")

            app.entry.delete(0, tk.END)
        else:
            app.label.configure(text="Not a video!", text_color="red")
            app.update()
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
            app.update()

    # channel or playlist
    if (((app.is_playlist.get() == 1) or (app.is_channel.get() == 1)) and (not get_list_of_videos)):
        if (link.find("list") != -1) or (link.find("/c") != -1) or (link.find("/@") != -1):

            list_type = ""
            playlist = None
            list_name = ""

            if (link.find("list") != -1):
                playlist = Playlist(link)
                list_name = playlist.title
                list_type = "playlist"
            else:
                playlist = Channel(link)
                list_name = playlist.channel_name
                list_type = "channel"

            clipboard.copy("")
            msg = f'Number of videos in {list_type}: {len(playlist.video_urls)}'
            print(msg)
            app.label.configure(msg)
            app.update() 
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
            app.update() 

            playlist_download_thread = threading.Thread(target=playlist_download, daemon = True, args=[playlist])
            playlist_download_thread.start()

            app.entry.delete(0, tk.END)
        else:
            app.label.configure(text="Not a playlist!", text_color="red")
            app.is_playlist.deselect()
            app.update()
            time.sleep(1)
            app.label.configure(text="Link", text_color="white")
            app.update()

def playlist_download(playlist: Playlist):
    for url in playlist.video_urls:
        time.sleep(1.5)
        download_thread = threading.Thread(target=download_video, daemon = True, args=[url])
        download_thread.start()

def start_work(video_list=False):
    global get_list_of_videos
    
    get_list_of_videos = video_list
    work_thread = threading.Thread(target=download_work, daemon = True)
    work_thread.start()

class SimpleYTD(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SimpleYTD")
        self.geometry("1000x600")
        self.iconphoto(False, tk.PhotoImage(file=relative_to_assets('icon.png')))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.button_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.button_frame.grid(row=0, column=0, pady=(0, 0), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(4, weight=1)    

        self.logo_label = customtkinter.CTkLabel(self.button_frame, text="SimpleYTD", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.download_btn = customtkinter.CTkButton(
            master=self.button_frame,
            text="Download",
            command=start_work,
        )
        self.download_btn.grid(row=1, column=0, pady=(5, 0))

        self.select_folder_btn = customtkinter.CTkButton(
            master=self.button_frame,
            text="Select Download Folder",
            command=self.selectfolder,
        )
        self.select_folder_btn.grid(row=2, column=0, pady=(5, 0))

        self.get_list_of_videos_btn = customtkinter.CTkButton(
            master=self.button_frame,
            text="Get list of videos",
            command=lambda: start_work(True),
        )
        self.get_list_of_videos_btn.grid(row=3, column=0, pady=(5, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 20))

        self.entry_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry_frame.grid_columnconfigure(0, weight=1)     

        self.label = customtkinter.CTkLabel(self.entry_frame, text="Link", anchor="w")
        self.label.grid(row=0, column=0, padx=20, pady=(0, 0))
        self.entry = customtkinter.CTkEntry(self.entry_frame, width=550)
        self.entry.grid(row=1, column=0)
        self.entry.bind("<Enter>", self.pastelink)

        # create textbox (for debugging)
        self.textbox = customtkinter.CTkTextbox(self, width=250, font=('Courier', 12))
        
        # create queue frame
        self.queue_frame = customtkinter.CTkScrollableFrame(self.entry_frame)
        self.queue_frame.grid(row=2, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.queue_frame.grid_columnconfigure(0, weight=1)

        # create options frame
        self.options_frame = customtkinter.CTkScrollableFrame(self, label_text="Options")
        self.options_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.options_frame.grid_columnconfigure(0, weight=1)

        self.convert_to_mp3 = customtkinter.CTkSwitch(master=self.options_frame, text="Convert to MP3?")
        self.convert_to_mp3.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.is_playlist = customtkinter.CTkSwitch(master=self.options_frame, text="Playlist?")
        self.is_playlist.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.is_channel = customtkinter.CTkSwitch(master=self.options_frame, text="Channel?")
        self.is_channel.grid(row=2, column=0, padx=10, pady=(0, 20))

        # only one can be selected at a time
        self.is_playlist.configure(command=self.is_channel.deselect)
        self.is_channel.configure(command=self.is_playlist.deselect)

        # register on click event
        self.bind("<Button-1>", self.on_click)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.configure(state="disabled")

        self.timer_active = False
        self.box_visible = False
        self.download_tooltip = None
        self.folderpath = ""
    
    def selectfolder(self):
        self.folderpath = filedialog.askdirectory(mustexist=False)
        text = "Selected folder: " + self.folderpath
        if not app.download_tooltip == None:
            app.download_tooltip.set_text(text)
        else:
            app.download_tooltip = ToolTip(app.select_folder_btn, text)

    def pastelink(self, event):
        clipboard_text = clipboard.paste()
        if(clipboard_text.find("youtube") != -1):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, clipboard_text)
            self.update()
        else:
            self.entry.delete(0, tk.END)

    def timer_end(self):
        self.timer_active = False

    def on_click(self, event: tk.Event):
        x = event.x_root - self.winfo_rootx()
        y = event.y_root - self.winfo_rooty()

        if (x > 0 and y > 0) and (x < 20 and y < 20):
            self.timer_active = True
            timer = threading.Timer(5.0, self.timer_end)
            timer.start()

        if (x > (self._current_width - 20) and y > (self._current_height - 20)) and (x < self._current_width and y < self._current_height):
            if self.timer_active:
                if not self.box_visible:
                    self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
                    self.box_visible = True
                else:
                    self.textbox.grid_remove()
                    self.box_visible = False

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        if not self.box_visible:
            self.textbox.grid_remove()

    def on_closing(self):
        self.destroy()
        exit()

if __name__ == "__main__":
    logger = PrintLogger()
    sys.stdout = logger
    sys.stderr = logger
    app = SimpleYTD()
    app.mainloop()