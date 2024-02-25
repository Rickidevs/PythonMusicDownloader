from tkinter import *
import customtkinter
import tempfile, base64, zlib
from pytube import YouTube
import requests
from PIL import Image,ImageTk,ImageOps,ImageDraw 
import os
from pathlib import Path
import threading
from CTkMessagebox import CTkMessagebox


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


#Fonts for text and button
FONT_1=("Arial",25,"bold")
FONT_2=("Arial",50,"bold")
FONT_3=("Arial",30,"bold")
FONT_4=("Arial",15)
FONT_5=("Arial",16,"bold")
FONT_6=("Times New Roman",20,"bold")
FONT_7=("Arial",13)

#global variable
music_thub = ""
music_title=""
yt = ""
url = ""
music_title_label = ""
music_thub_label = ""

#booleans
is_search = False
is_download = False
exists_ok = False


def do_download(url): 
    try:
        global exists_ok,is_download
        path_to_download = str(os.path.join(Path.home(), 'Downloads'))
        path_to_check = os.path.expanduser("~/Downloads")
        music_mp3 =f"{music_title}.mp3"
        path_exists = os.path.exists(os.path.join(path_to_check,music_mp3))
        if path_exists == True:
            CTkMessagebox(title="Warning!",icon="warning", message="This file already exists!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
        else:
            loading_label = customtkinter.CTkLabel(master=screen,text="Please wait, Downloading...",font=FONT_1)
            loading_label.place(x=20,y=390)
            stream = yt.streams.filter(only_audio=True).first()
            downloaded_file = stream.download(path_to_download)
            base, ext = os.path.splitext(downloaded_file)
            new_file = base + '.mp3'
            os.rename(downloaded_file, new_file)
            loading_label.configure(text="")
            is_download = False
            copleted_label = customtkinter.CTkLabel(master=screen,text=f"Completed: {path_to_download}",font=FONT_5,wraplength=300)
            copleted_label.place(x=20,y=390)
    except Exception as e:
        print(f"Download error: {e}") 

def start_download_thread():
    global is_download
    if is_download == True:
         CTkMessagebox(title="Warning!",icon="warning", message="Download is already in progress!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
    else:
        is_download = True
        thread = threading.Thread(target=do_download, args=(url,))
        thread.start()

def about_music():
      global music_title_label, music_thub_label,url
      url = music_thub
      image = Image.open(requests.get(url, stream=True).raw)
      new_size = (170, 140)

# Köşeleri yuvarlatma fonksiyonu
      def round_corners(im, radius):
            circle = Image.new('L', (radius * 2, radius * 2), 0)  # Siyah daire oluşturun

            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)  # Beyaz elips ile doldur
            
            alpha = Image.new('L', im.size, 255)
            w, h = im.size
            alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
            alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
            alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
            alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
            im.putalpha(alpha)
            return im

    # Köşeleri yuvarlatılmış resim oluşturun
      transformed_image = round_corners(image.resize(new_size), 10)

      bg_modern_label = customtkinter.CTkFrame(master=screen,
                               width=380,
                               height=140,
                               fg_color="gray20",
                               border_width=2,
                               border_color="gray25",
                               corner_radius=20)
      bg_modern_label.place(x=10,y=240)

      tkimage = ImageTk.PhotoImage(transformed_image)
      music_thub_label = customtkinter.CTkLabel(master=screen,image=tkimage,text="")
      music_thub_label.place(x=20,y=250)
      music_title_label = customtkinter.CTkLabel(master=screen,bg_color="gray20",text=music_title,font=FONT_6,)
      music_symbol_label = customtkinter.CTkLabel(master=screen,bg_color='gray20',text="▶• ılıılıılıılıılıılı.",font=FONT_1)
      music_symbol_label.place(x=168,y=290)

      if len(music_title) > 20:
            music_edited_title = music_title[:20]
            music_title_label.configure(text=f"{music_edited_title}..")
            music_title_label.place(x=168, y= 250)
      else:
            music_title_label.place(x=168, y= 250)

      Download_button = customtkinter.CTkButton(master=screen,
                                 width=80,
                                 height=30,
                                 border_color="grey",
                                 border_width=2,
                                 corner_radius=13,
                                 fg_color="green",
                                 bg_color="gray20",
                                 text="Download",
                                 text_color="white",
                                 hover_color="light green",
                                 font=FONT_4,
                                 command=start_download_thread
                                 )
      Download_button.place(x=180,y=330)

def do_search():
    global url, is_search
    music_link = link_entry.get()
    if music_link == "":
        is_search = False
        CTkMessagebox(title="Warning!",icon="warning", message="Enter a link to search!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
    elif not music_link.startswith("https://youtu.be/"):
        is_search = False
        link_entry.delete(0, END)
        CTkMessagebox(title="Warning!",icon="warning", message="Enter a vaild Youtube music link!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
    else:
        searching_label = customtkinter.CTkLabel(master=screen,text="Please wait, Searching...",font=FONT_1)
        searching_label.place(x=20,y=390)
        link_entry.delete(0, END)
        global yt
        yt = YouTube(music_link)
        global music_title, music_thub
        music_thub = yt.thumbnail_url
        music_title = yt.title
        searching_label.configure(text="")
        is_search = False
        about_music()

def search_thread():
    global is_search, is_download
    if is_search == True:
        CTkMessagebox(title="Warning!",icon="warning", message="There is an ongoing process, please wait!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
    elif is_download == True:
        CTkMessagebox(title="Warning!",icon="warning", message="Download is already in progress!", option_1="OK",width=400,height=150, font=FONT_4,button_color="green",title_color="green",button_hover_color="light green",sound=ON, button_width= 10)
    else:
        is_search = True
        thread = threading.Thread(target=do_search)
        thread.start()


youtube_label = customtkinter.CTkLabel(master=screen,text="Youtube",font=FONT_1,text_color="green")
youtube_label.place(x=50,y=30)

music_label = customtkinter.CTkLabel(master=screen,text="Music",font=FONT_2,text_color="green")
music_label.place(x=70,y=55)

downloader_label = customtkinter.CTkLabel(master=screen,text="Downloader",font=FONT_3,text_color="green")
downloader_label.place(x=105,y=105)

link_entry = customtkinter.CTkEntry(master=screen,
                               placeholder_text="Enter Youtube music link!",
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
                                 command=search_thread
                                 )

search_button.place(x=290,y=180)


screen.mainloop()