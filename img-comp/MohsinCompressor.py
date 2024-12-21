from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def resize_and_compress_image(input_path, output_path, max_size, quality=85):
    """
    Resizes and compresses a single image.
    """
    try:
        print(f"Opening image: {input_path}")
        img = Image.open(input_path)
        img = img.convert("RGB")
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)  # Updated to use LANCZOS
        print(f"Saving compressed image to: {output_path}")
        img.save(output_path, "JPEG", quality=quality)
        print(f"Successfully processed: {input_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def process_images(input_folder, output_folder, max_size, quality):
    """
    Processes all images in the input folder, updating the progress bar.
    """
    if not os.path.exists(input_folder):
        messagebox.showerror("Error", f"Input folder '{input_folder}' does not exist!")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of files in the folder
    files = [f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"))]
    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo("Info", "No image files found in the input folder.")
        return

    # Update progress bar
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0
    progress_label.config(text=f"Progress: 0 / {total_files}")
    root.update_idletasks()

    # Process each file
    for index, filename in enumerate(files):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_compressed.jpg")
        try:
            resize_and_compress_image(input_path, output_path, max_size, quality)
        except Exception as e:
            print(f"Error processing {input_path}: {e}")

        # Update progress bar
        progress_bar["value"] = index + 1
        progress_label.config(text=f"Progress: {index + 1} / {total_files}")
        root.update_idletasks()

    messagebox.showinfo("Success", f"Mohsin Compressor processed {total_files} images!")


def select_input_folder():
    """
    Opens a folder dialog for selecting the input folder.
    """
    folder = filedialog.askdirectory(title="Select Input Folder")
    input_folder_var.set(folder)


def select_output_folder():
    """
    Opens a folder dialog for selecting the output folder.
    """
    folder = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder)


def start_compression():
    """
    Validates input and starts the compression process.
    """
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()

    try:
        max_size = int(max_size_var.get())
        quality = int(quality_var.get())
    except ValueError:
        messagebox.showerror("Error", "Max size and quality must be valid numbers!")
        return

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders!")
        return

    process_images(input_folder, output_folder, max_size, quality)


# GUI Setup
root = tk.Tk()
root.title("Mohsin Compressor")
root.geometry("500x300")
root.configure(bg="#eaf7fc")  # Light blue background

# Input Folder
tk.Label(root, text="Input Folder:", bg="#eaf7fc", fg="#333", font=("Helvetica", 12)).grid(
    row=0, column=0, padx=10, pady=5, sticky="e"
)
input_folder_var = tk.StringVar()
tk.Entry(root, textvariable=input_folder_var, width=40, font=("Helvetica", 10)).grid(
    row=0, column=1, padx=10, pady=5
)
tk.Button(
    root, text="Browse", command=select_input_folder, bg="#34c3eb", fg="white", font=("Helvetica", 10, "bold")
).grid(row=0, column=2, padx=10, pady=5)

# Output Folder
tk.Label(root, text="Output Folder:", bg="#eaf7fc", fg="#333", font=("Helvetica", 12)).grid(
    row=1, column=0, padx=10, pady=5, sticky="e"
)
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=40, font=("Helvetica", 10)).grid(
    row=1, column=1, padx=10, pady=5
)
tk.Button(
    root, text="Browse", command=select_output_folder, bg="#34c3eb", fg="white", font=("Helvetica", 10, "bold")
).grid(row=1, column=2, padx=10, pady=5)

# Max Size
tk.Label(root, text="Max Size (px):", bg="#eaf7fc", fg="#333", font=("Helvetica", 12)).grid(
    row=2, column=0, padx=10, pady=5, sticky="e"
)
max_size_var = tk.StringVar(value="800")
tk.Entry(root, textvariable=max_size_var, width=10, font=("Helvetica", 10)).grid(
    row=2, column=1, padx=10, pady=5, sticky="w"
)

# Quality
tk.Label(root, text="Quality (1-100):", bg="#eaf7fc", fg="#333", font=("Helvetica", 12)).grid(
    row=3, column=0, padx=10, pady=5, sticky="e"
)
quality_var = tk.StringVar(value="80")
tk.Entry(root, textvariable=quality_var, width=10, font=("Helvetica", 10)).grid(
    row=3, column=1, padx=10, pady=5, sticky="w"
)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

progress_label = tk.Label(root, text="Progress: 0 / 0", bg="#eaf7fc", font=("Helvetica", 10))
progress_label.grid(row=5, column=0, columnspan=3)

# Start Button
tk.Button(
    root,
    text="Start Compression",
    command=start_compression,
    bg="#f76d42",
    fg="white",
    font=("Helvetica", 12, "bold"),
).grid(row=6, column=0, columnspan=3, pady=20)

root.mainloop()
