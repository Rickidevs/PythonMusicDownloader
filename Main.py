from tkinter import *
import customtkinter
import tempfile, base64, zlib
from pytube import YouTube
import requests
import time
from PIL import Image,ImageTk
import os
from pathlib import Path


# for remove tk iconbit
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)




# Set windows and configure
screen = customtkinter.CTk()
screen.geometry("400x500")
customtkinter.set_appearance_mode("dark")
screen.title("Youtube Music Downloader")
screen.iconbitmap(default=ICON_PATH)
screen.resizable(False, False)

FONT_1=("Arial",25,"bold")
FONT_2=("Arial",50,"bold")
FONT_3=("Arial",30,"bold")
FONT_4=("Arial",15)
FONT_5=("Arial",16,"bold")
FONT_6=("Times New Roman",20,"bold")

music_thub = ""
music_title=""
music_views=""
music_rating=""
yt = ""

def toplevel_screen():
            
            toplevel = customtkinter.CTkToplevel(screen)  # Pass the main window as the parent
            toplevel.title("WARNING")
            toplevel.geometry("+%d+%d" % (screen.winfo_x()+90, screen.winfo_y()+240))
            toplevel.geometry("250x100")
            toplevel.resizable(False, False)
            label = customtkinter.CTkLabel(toplevel, text="invalid Youtube link!\nTry again with a valid link :)", font=FONT_5)
            label.pack(padx=20, pady=20)
            toplevel.grab_set()

def download_music():
      
      path_to_download = str(os.path.join(Path.home(), 'Downloads'))
      stream=yt.streams.filter(only_audio=True).first()
      downloaded_file = stream.download(path_to_download)
      base, ext = os.path.splitext(downloaded_file)
      new_file = base + '.mp3'
      os.rename(downloaded_file, new_file)
      copleted_label = customtkinter.CTkLabel(master=screen,text=f"Completed. You can find it in this: {path_to_download}",font=FONT_5,wraplength=300)
      copleted_label.place(x=30,y=360)


def about_music():
      url = music_thub
      image = Image.open(requests.get(url, stream=True).raw)
      new_size = (170, 140)  
      resized_image = image.resize(new_size) 
      tkimage = ImageTk.PhotoImage(resized_image)
      music_thub_label = customtkinter.CTkLabel(master=screen,image=tkimage)
      music_thub_label.place(x=20,y=230)
      music_title_label = customtkinter.CTkLabel(master=screen,text=music_title,font=FONT_6,wraplength=200)
      music_title_label.place(x=168, y= 230)
      Download_button = customtkinter.CTkButton(master=screen,
                                 width=80,
                                 height=30,
                                 border_color="grey",
                                 border_width=2,
                                 corner_radius=13,
                                 fg_color="green",
                                 text="Download",
                                 text_color="white",
                                 hover_color="light green",
                                 font=FONT_4,
                                 command=download_music
                                 )
      Download_button.place(x=180,y=310)

def search_button():
        music_link = link_entry.get()
        if music_link == "":
            toplevel_screen()
        elif not music_link.startswith("https://youtu.be/"):
            link_entry.delete(0, END)
            toplevel_screen()
        else:
            link_entry.delete(0, END)
            global yt
            yt = YouTube(music_link)
            global music_title,music_thub
            music_title = yt.title
            music_thub = yt.thumbnail_url
            about_music()


                

youtube_label = customtkinter.CTkLabel(master=screen,text="Youtube",font=FONT_1,text_color="green")
youtube_label.place(x=50,y=30)

music_label = customtkinter.CTkLabel(master=screen,text="Music",font=FONT_2,text_color="green")
music_label.place(x=70,y=55)

downloader_label = customtkinter.CTkLabel(master=screen,text="Downloader",font=FONT_3,text_color="green")
downloader_label.place(x=105,y=105)



link_entry = customtkinter.CTkEntry(master=screen,
                               placeholder_text="Enter Youtube music link",
                               width=260,
                               height=35,
                               border_width=2,
                               corner_radius=10)

link_entry.place(x=20,y=180)

search_button = customtkinter.CTkButton(master=screen,
                                 width=80,
                                 height=35,
                                 border_color="grey",
                                 border_width=2,
                                 corner_radius=10,
                                 fg_color="green",
                                 text="Search",
                                 text_color="white",
                                 hover_color="light green",
                                 font=FONT_4,
                                 command=search_button
                                 )

search_button.place(x=290,y=180)


screen.mainloop()