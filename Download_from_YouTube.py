from pytube import YouTube

from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showwarning, showinfo

import os

window = Tk()
# window.overrideredirect(True)
window.title("Download video from YouTube!")

window.iconbitmap('ico.ico')


window.geometry("500x500")
window.resizable(width=False, height=False)

canvas = Canvas(window, width=500, height=500)
canvas.pack()

logo = PhotoImage(file='youtube.png')
logo = logo.subsample(16, 16)
canvas.create_image(245, 85, image=logo)

label = ttk.Label(window, text='Type link video you want to download', font='Times 15')
canvas.create_window(250, 200, window=label)

urlEnter = ttk.Entry(window, width=35, font='Times 15')
canvas.create_window(250, 233, window=urlEnter)

find_button = Button(window, text='Find resolutions', height=2, width=13, fg='#ffffff', background='#ff0000')
canvas.create_window(140, 310, window=find_button)

resolution_label = ttk.Label(window, text='Resolutions:', font='Times 12')
canvas.create_window(140, 350, window=resolution_label)

video_resolution = ttk.Combobox(window, width=10)
canvas.create_window(140, 372, window=video_resolution)

download_button = Button(window, text='Download Video', height=3, width=15, background='#ff0000', fg='#ffffff')
canvas.create_window(352, 318, window=download_button)

download_audio_button = Button(window, text='Download audio', height=1, width=15, background='#ff0000', fg='#ffffff')
canvas.create_window(352, 370, window=download_audio_button)

########################
download_location_var = StringVar()
download_location_var.set(os.getcwd())

download_location_label = ttk.Label(window, text="Download Location:", font='Times 12')
canvas.create_window(180, 420, window=download_location_label)

download_location_entry = Entry(window, textvariable=download_location_var, width=35, font='Times 12')
canvas.create_window(250, 450, window=download_location_entry)

download_location_button = Button(window, text="Select Folder", height=1, width=15, background='#ff0000', fg='#ffffff')
canvas.create_window(322, 420, window=download_location_button)


########################

def open_file_dialog():
    folder_selected = filedialog.askdirectory()
    download_location_var.set(folder_selected)


download_location_button.configure(command=open_file_dialog)


def find_resolutions():
    yt = urlEnter.get()

    if yt == "":
        showerror(title="Error", message="Input field is empty")

    else:
        link = YouTube(yt)

        resolutions = []
        for i in link.streams.filter():
            if i.resolution != None:
                resolutions.append(i.resolution)

        resolutions = sorted(list((set(resolutions))))

        video_resolution['values'] = resolutions


find_button.configure(command=find_resolutions)


def download_video():
    yt_url = urlEnter.get()

    if yt_url == "":
        showerror(title="Error", message="Input field is empty")
        return

    link = YouTube(yt_url)

    if not link.streams:
        showerror(title="Error", message="Ups...")
        return

    if video_resolution.get() == '':
        showerror(title="Error", message="Select resolution")
        return

    resolution = video_resolution.get()
    if link.streams.filter(resolution=resolution).first() != None:
        try:
            output_path = os.path.join(download_location_var.get(), 'Download from YouTube')

            video = link.streams.filter(resolution=resolution).first()

            if os.path.isfile(output_path+ "\\" + video.title + " " + resolution + ".mp4"):
                showerror(title="Error", message="Video already exists")
                return

            video.download(output_path=output_path, filename= video.title + " " + resolution + ".mp4")

            showinfo(title="Download video", message="Video downloaded successfully")

        except FileExistsError:
            showerror(title="Error", message="Video already exists")
            return
    else:
        showerror(title="Error", message="Invalid video resolution")
download_button.configure(command=download_video)


def download_audio():
    yt_url = urlEnter.get()

    if yt_url == "":
        showerror(title="Error", message="Input field is empty")
        return

    link = YouTube(yt_url)

    if not link.streams:
        showerror(title="Error", message="Ups...")
        return

    try:
        output_path = os.path.join(download_location_var.get(), 'Download from YouTube')

        audio = link.streams.get_audio_only()

        if os.path.isfile(output_path + "\\" + link.title + ".mp3"):
            showerror(title="Error", message="Audio already exists")
            return

        audio.download(output_path=output_path, filename= link.title + ".mp3")

        showinfo(title="Download audio", message="Audio downloaded successfully")
    except FileExistsError:
        showerror(title="Error", message="Audio already exists")


download_audio_button.configure(command=download_audio)

window.mainloop()
