import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import re
from tkinter import messagebox
from PIL import Image
import sys

window = tk.Tk()
window.title("Image Compressor")
window.geometry("400x475")
window.resizable(width=False, height=False)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

iconPath = resource_path('Icon.ico')
window.iconbitmap(iconPath)

def browse_action():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)
        get_images()
def browse_action_button():
    browse_action()
def browse_action_entry(event):
    browse_action()
def ignore_key(event):
    return "break"


def get_images():
    path = folder_entry.get()
    if path:
        multiple_images = [file for file in os.listdir(path)]
        total = len(multiple_images)
        file_names=""
        label1.config(text=str(total)+ " images detected!")


def is_valid_filename(filename: str) -> bool:
    # Check if the file name is empty
    if not filename:
        return False

    # Check if the file name contains any invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False

    # Check if the file name ends with a period or space
    if filename[-1] in ['.', ' ']:
        return False

    return True

def file_name_leave(event):
    file_name = file_name_entry.get()
    if file_name:
        if not is_valid_filename(file_name):
            messagebox.showerror("File Name Error", "The file name is invalid.")
            file_name_entry.delete(0, 'end')
            file_name_entry.insert(0, 'Compressed')
            window.focus()
    else:
        file_name_entry.insert(0, 'Compressed')
        window.focus()

def file_name_radio():
    if radio_original_var.get() == 1:
        file_name_entry.config(state=tk.NORMAL)
        new_file_name_part.config(state=tk.NORMAL)
        label2.config(state=tk.NORMAL)
        file_name_entry.focus()
    else:
        file_name_entry.config(state=tk.DISABLED)
        new_file_name_part.config(state=tk.DISABLED)
        label2.config(state=tk.DISABLED)
        window.focus()



def update_progress_bar(progress):
    progress_bar['value'] = progress
    label_percent.config(text=str(progress) + '%')
    window.update_idletasks()

def progress(progress_var):
    if progress_var < 100:
        update_progress_bar(progress_var)
    if progress_var == 100:
        update_progress_bar(progress_var)
        label_process.config(text="Compression Completed!")
        messagebox.showinfo(message='The progress completed!')

def compress_action():
    if folder_entry.get():
        quality = selected_quality.get()
        #["Small", "HD", "Full HD","Ultra HD"]
        screen_width =1920
        if quality == "Small":
            screen_width = 640
        elif quality == "HD":
            screen_width = 1280
        elif quality == "Full HD":
            screen_width = 1920
        elif quality == "Ultra HD":
            screen_width = 3840

        file_name_replacing = radio_original_var.get()

        path = folder_entry.get()
        directory_files = os.listdir(path)
        
        multiple_images = [file for file in directory_files if file.endswith(('.jpg', '.png'))]

        total = len(multiple_images)

        label_process.config(text="Compressing...")

        original_size = 0.00
        new_size = 0.0

        for i in range(total):
            try:
                image_name = path+"/"+multiple_images[i]
                new_file_name = image_name
                if file_name_replacing == 1:
                    new_file_name = path+"/"+file_name_entry.get() + " - " + multiple_images[i]
                image = Image.open(image_name)
                image_width, image_height = image.size
                original_size += os.path.getsize(image_name)
                if image_width > screen_width or image_height > screen_width:
                    qsize = screen_width
                    exif_data = image.info['exif']
                    if image_width > image_height:
                        wsize = qsize
                        width_percent = (qsize / image_width)
                        hsize = int((float(image_height) * float(width_percent)))
                    else:
                        hsize = qsize
                        height_percent = (qsize / image_height)
                        wsize = int((float(image_width) * float(height_percent)))
                    image = image.resize((wsize, hsize))
                    image.save(new_file_name, 'JPEG', exif=exif_data)
            except:
                pass
            new_size += os.path.getsize(image_name)
            image.close()
            compression_progress = round((((i + 1) / total) * 100),1)
            label_initial_file_size.config(text="Initial File Size: {:0.2f}MB".format(original_size / (1024 * 1024)))
            label_final_file_size.config(text="Final File Size: {:0.2f}MB".format(new_size / (1024 * 1024)))
            label_compression_ratio.config(text="Compression Ratio: {:0.2f}%".format(((original_size-new_size) / original_size) * 100))
            progress(compression_progress)
    else:
        messagebox.showerror("Folder Error",message="Please select a folder first!")

def finish_action():
    window.destroy()

select_folder_label = ttk.Label(text="Select the folder")
select_folder_label.pack(padx=10, pady=(10,0), anchor="w")

select_folder_frame = tk.Frame(relief=tk.SUNKEN, borderwidth=0)
select_folder_frame.pack(padx=(0,10), pady=(0,5), fill=tk.X)

folder_entry = ttk.Entry(select_folder_frame)
folder_entry.pack(padx=(10,5), pady=0, anchor="w", fill=tk.X, expand=True, side=tk.LEFT)
folder_entry.bind("<1>", browse_action_entry)
folder_entry.bind("<Key>", ignore_key)

button = ttk.Button(select_folder_frame,text="Browse", command=browse_action_button)
button.pack(side=tk.RIGHT)

label1 = ttk.Label(text="Image files in the selected folder: ",width=tk.X, )
label1.pack(padx=10, pady=(0,10), anchor="w")

compress_settings_frame = ttk.LabelFrame(text="Compression Settings", borderwidth=1, border=5)
compress_settings_frame.pack(padx=(10,10), pady=(0,5), fill=tk.X)

compress_settings_frame.grid_columnconfigure(0, weight=1, uniform="column")
compress_settings_frame.grid_columnconfigure(1, weight=2, uniform="column")
compress_settings_frame.grid_rowconfigure(0, weight=1)
compress_settings_frame.grid_rowconfigure(1, weight=1)
compress_settings_frame.grid_rowconfigure(3, weight=1)

radio_original_var = tk.IntVar()
radio_original_var.set(2)

radio_original = ttk.Radiobutton(compress_settings_frame, text="Keep Originals", variable=radio_original_var, value=1, command=file_name_radio)
radio_original.grid(row=0, column=0, padx=5, pady=0, sticky="w")

radio_replace = ttk.Radiobutton(compress_settings_frame, text="Replace Originals", variable=radio_original_var, value=2, command=file_name_radio)
radio_replace.grid(row=1, column=0, padx=5, pady=(0,5), sticky="w")

label2 = ttk.Label(compress_settings_frame,text="New File Name:")
label2.grid(row=0, column=1, padx=(15,10), pady=0, sticky="w")

file_name_frame = tk.Frame(compress_settings_frame)
file_name_frame.grid(row=1, column=1, padx=10, pady=0, sticky="w")

file_name_frame.grid_columnconfigure(0, weight=1)
file_name_frame.grid_columnconfigure(1, weight=1)
file_name_frame.grid_columnconfigure(2, weight=1)

file_name_entry = ttk.Entry(file_name_frame, width=15, text="Compressed")
file_name_entry.grid(row=0, column=0, padx=(5,5), pady=(0,5), sticky="w")
file_name_entry.insert(0, 'Compressed')

file_name_entry.bind("<Leave>", file_name_leave)

new_file_name_part= ttk.Label(file_name_frame,text="- Original File Name")
new_file_name_part.grid(row=0, column=1,columnspan=2, padx=(0,5), pady=(0,5), sticky="w")

file_name_radio()

label3 = ttk.Label(compress_settings_frame,text="Compression Size:")
label3.grid(row=2, column=0, padx=5, pady=(5,5), sticky="w")

selected_quality = tk.StringVar()
options = ["Small", "HD", "Full HD","Ultra HD"]

compression_sizes_option_menu = ttk.OptionMenu(compress_settings_frame, selected_quality, options[2], *options)
compression_sizes_option_menu.grid(row=2, column=1, padx=10, pady=(5,5), sticky="w")
compression_sizes_option_menu.config(width=15)


compress_button = ttk.Button(window,text="Compress", command=compress_action)
compress_button.pack(padx=10, pady=(0,10), anchor="n", fill=tk.X)


progress_bar_frame = ttk.LabelFrame(text="Process", borderwidth=1, border=5)
progress_bar_frame.pack(padx=(10,10), pady=(0,5), fill=tk.X)

progress_bar = ttk.Progressbar(progress_bar_frame, orient="horizontal", length=50, mode="determinate")
progress_bar.pack(padx=0, pady=5, fill=tk.X)

label_percent = ttk.Label(progress_bar_frame, text="0%", width=tk.X)
label_percent.pack(padx=10, pady=(0, 0), anchor="n")

label_process = ttk.Label(progress_bar_frame,text="Waiting!", width=tk.X)
label_process.pack(padx=10, pady=(0, 5), anchor="n")

output_frame = ttk.LabelFrame(text="Output", borderwidth=1, border=5)
output_frame.pack(padx=(10,10), pady=(0,5), fill=tk.X)

label_initial_file_size = ttk.Label(output_frame,text="Initial File Size: 0 MB")
label_initial_file_size.pack(padx=10, pady=(0, 5), anchor="w")

label_final_file_size = ttk.Label(output_frame,text="Final File Size: 0 MB")
label_final_file_size.pack(padx=10, pady=(0, 5), anchor="w")

label_compression_ratio = ttk.Label(output_frame,text="Compression Ratio: 0%")
label_compression_ratio.pack(padx=10, pady=(0, 5), anchor="w")

finish_button = ttk.Button(window,text="Exit", command=finish_action)
finish_button.pack(padx=10, pady=(0,10), anchor="n", fill=tk.X)

window.mainloop()