from tkinter import *
from pygame import *
from tkinter import filedialog as fd
from mutagen.mp3 import *

from tkinter import ttk
from ttkthemes import themed_tk as tk

import time
import tkinter.messagebox as tm
import os
import threading

# creating the windows and importing the themes
windows = tk.ThemedTk()
windows.get_themes()
windows.set_theme("arc")
windows.title("D.Reaper")
# windows.geometry('300x300')
windows.iconbitmap(r'icon/multi.ico')

# initializing the mixer function
mixer.init()

# declaring the logic behind the pause and mue button
paused = FALSE
muted = FALSE
playlist = []

# creating the status bar
stat = Label(windows, text="Welcome to D.Reaper's studio", relief=SUNKEN, anchor=W, font='Times 10 italic')
stat.pack(side=BOTTOM, fill=X)

# function to add a music file


def add_music():
    global file_path
    file_path = fd.askopenfilename()

    make_playlist(file_path)


# the menu bar for the "about us"

def about_us():
    tm.showinfo("About D.Reaper", "There's nothing special here, I just wanted to add more things to my menu")

# creating the space in the windows for the menu bar


mymenu = Menu(windows)
windows.config(menu=mymenu)

# creating the actual menus and submenus
file = Menu(mymenu, tearoff=0)
mymenu.add_cascade(label="File", menu=file)
file.add_command(label="Add music", command=add_music)

file.add_separator()

helps = Menu(mymenu, tearoff=0)
mymenu.add_cascade(label="Help", menu=helps)
helps.add_command(label="About us", command=about_us)


# the function to remove music from the playlist and from the memory

def rem_music():
    try:
        select_song = lst1.curselection()
        select_song = int(select_song[0])
        lst1.delete(select_song)
        playlist.pop(select_song)
    except Exception:
        tm.showerror("Can't find track", "Please select a track to remove from playlist")


# the function to add music to the playlist

def make_playlist(file_name):
    file_name = os.path.basename(file_name)
    j = 0
    playlist.insert(j, file_path)
    lst1.insert(j, file_name)
    j += 1


# the function to play and un-pause music

def play():
    global paused
    if paused:
        mixer.music.unpause()
        paused = FALSE
    else:
        try:
            stop()
            time.sleep(1)
            select_song = lst1.curselection()
            select_song = int(select_song[0])
            play = playlist[select_song]
            mixer.music.load(play)
            mixer.music.play()
            stat['text'] = os.path.basename(play)
            text['text'] = "Playing: " + os.path.basename(play)
            track_len(play)
        except:
            tm.showerror("Track not found", "Select a track")


# the function to pause music

def pause():
    global paused
    mixer.music.pause()
    paused = TRUE


# the function to stop music

def stop():
    mixer.music.stop()
    text['text'] = "Play music"
    stat['text'] = "Welcome to D.Reaper's studio"
    text2['text'] = "Track length: --:--"
    text3['text'] = "Current time: --:--"


# the function for the volume button

def set_vol(volume):
    myvol = float(volume) / 100
    mixer.music.set_volume(myvol)


def mute():
    global muted
    if muted:
        vol.set(50)
        mixer.music.set_volume(50 / 100)
        button4.configure(image=photo4)
        muted = FALSE
    else:
        vol.set(0)
        mixer.music.set_volume(0)
        button4.configure(image=photo5)
        muted = TRUE


def track_len(songg):
    tot_len = os.path.splitext(songg)

    if tot_len[1] == '.mp3':
        audio = MP3(songg)
        trac_len = audio.info.length
    else:
        a = mixer.Sound(songg)
        trac_len = a.get_length()

    mins, secs = divmod(trac_len, 60)
    mins = round(mins)
    secs = round(secs)
    lenth = '{:02d}:{:02d}'.format(mins, secs)
    text2['text'] = "Track length: " + lenth

    t1 = threading.Thread(target=current, args=(trac_len,))
    t1.start()


left_frame = Frame(windows)
left_frame.pack(side=LEFT, pady=20, padx=25)

bottom_frame2 = Frame(left_frame)
bottom_frame2.pack(side=BOTTOM)


def current(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            lenth = '{:02d}:{:02d}'.format(mins, secs)
            text3['text'] = "Current time: " + lenth

            time.sleep(1)

            t -= 1


right_frame = Frame(windows)
right_frame.pack(side=RIGHT)

top_frame = Frame(right_frame)
top_frame.pack(pady=10)

middle_frame = Frame(right_frame)
middle_frame.pack(pady=10, padx=15)

bottom_frame = Frame(right_frame)
bottom_frame.pack(pady=20)


text = ttk.Label(top_frame, text="Play music")
text.pack(pady=5)

text2 = ttk.Label(top_frame, text="Track length: --:--")
text2.pack()

text3 = ttk.Label(top_frame, text="Current time: --:--", relief=GROOVE)
text3.pack(pady=5)

photo1 = PhotoImage(file="icon/play3.png")
button1 = ttk.Button(middle_frame, image=photo1, command=play)
button1.pack(side=LEFT, padx=5)

photo2 = PhotoImage(file="icon/pause3.png")
button2 = ttk.Button(middle_frame, image=photo2, command=pause)
button2.pack(side=LEFT, padx=5)

photo3 = PhotoImage(file="icon/stop2.png")
button3 = ttk.Button(middle_frame, image=photo3, command=stop)
button3.pack(side=LEFT, padx=5)

photo4 = PhotoImage(file="icon/speaker.png")
photo5 = PhotoImage(file="icon/mute2.png")
button4 = ttk.Button(bottom_frame, image=photo4, command=mute)
button4.pack(side=LEFT)

photo6 = PhotoImage(file="icon/addmusic2.png")
add_button = ttk.Button(bottom_frame2, image=photo6, command=add_music)
add_button.pack(side=LEFT)

photo7 = PhotoImage(file="icon/remmusic2.png")
remove_butt = ttk.Button(bottom_frame2, image=photo7, command=rem_music)
remove_butt.pack()


vol = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol.set(50)
mixer.music.set_volume(50/100)
vol.pack(pady=10)


lst1 = Listbox(left_frame, width=30, height=10)
lst1.pack(padx=15)


def close_win():
    stop()
    windows.quit()


windows.protocol("WM_DELETE_WINDOW", close_win)

file.add_command(label="Exit", command=close_win)

windows.mainloop()
