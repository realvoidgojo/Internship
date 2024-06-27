import tkinter as tk
from tkinter import ttk, Label, Button, filedialog, messagebox, Entry, font 
from PIL import ImageTk, Image
import cv2
import numpy as np

# Global vars
panelA = None
panelB = None
selected_image_path = None
filename = None
image_encrypted = None
key = None

def browse_image():
    global selected_image_path, panelA, path_entry
    filetypes = [("Image files", "*.png"),
                 ("Image files", "*.jpeg"),
                 ("Image files", "*.jpg")]

    filename = filedialog.askopenfilename(title="Select an image", filetypes=filetypes)
    if filename:
        selected_image_path = filename
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_image_path)
        original_image = Image.open(selected_image_path)
        original_image = original_image.resize((250, 250), Image.LANCZOS)  # Updated resize method
        img = ImageTk.PhotoImage(original_image)
        if panelA is None:
            panelA = tk.Label(image=img)
            panelA.image = img
            panelA.pack(side="left", padx=40, pady=15)
            panelA_placeholder.pack_forget()
        else:
            panelA.configure(image=img)
            panelA.image = img
            panelA_placeholder.pack_forget()

def transform_image():
    mode = mode_var.get()
    if mode == "Encryption":
        encryption()
    elif mode == "Decryption":
        decryption()

def encryption():
    global selected_image_path, panelB, image_encrypted, key
    if selected_image_path:
        image_input = cv2.imread(selected_image_path)
        if image_input is not None:
            (x, y, z) = image_input.shape
            image_input = image_input.astype(float) / 255.0
            mu, sigma = 0, 0.1
            key = np.random.normal(mu, sigma, (x, y, z)) + np.finfo(float).eps
            # print(key)
            image_encrypted = image_input / key
            cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
            img_encrypted = Image.open('image_encrypted.jpg')
            img_encrypted = img_encrypted.resize((250, 250), Image.LANCZOS)
            img_encrypted = ImageTk.PhotoImage(img_encrypted)
            if panelB is None:
                panelB = tk.Label(image=img_encrypted)
                panelB.image = img_encrypted
                panelB.pack(side="right", padx=40, pady=15)
                panelB_placeholder.pack_forget()
            else:
                panelB.configure(image=img_encrypted)
                panelB.image = img_encrypted
                panelB_placeholder.pack_forget()
            messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")
        else:
            messagebox.showwarning("Warning", "Failed to read image.")
    else:
        messagebox.showwarning("Warning", "No image selected.")

def decryption():
    global image_encrypted, key, panelB
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        # print(image_encrypted)
        # print(key)
        # print(image_output)
        image_output *= 255.0
        cv2.imwrite('image_output.jpg', image_output)
        img_decrypted = Image.open('image_output.jpg')
        img_decrypted = img_decrypted.resize((250, 250), Image.LANCZOS)  
        img_decrypted = ImageTk.PhotoImage(img_decrypted)
        if panelB is None:
            panelB = tk.Label(image=img_decrypted)
            panelB.image = img_decrypted
            panelB.pack(side="right", padx=40, pady=1)
            panelB_placeholder.pack_forget()
        else:
            panelB.configure(image=img_decrypted)
            panelB.image = img_decrypted
            panelB_placeholder.pack_forget()
        messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
    else:
        messagebox.showwarning("Warning", "Image not encrypted yet.")

def reset():
    global panelA, panelB, selected_image_path, path_entry
    selected_image_path = None
    path_entry.delete(0, tk.END)

    if panelA is not None:
        panelA.pack_forget()
        panelA_placeholder.pack(side="left", padx=40, pady=15)
        panelA = None

    if panelB is not None:
        panelB.pack_forget()
        panelB_placeholder.pack(side="right", padx=40, pady=15)
        panelB = None

    messagebox.showinfo("Success", "Reset to initial state!")

def save_image():
    global panelB
    if panelB is not None and panelB.image:
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            panelB.image.write(filename)
            messagebox.showinfo("Save Status", "Image saved successfully.")
    else:
        messagebox.showwarning("Warning", "No image to save.")

# Create main window
root = tk.Tk()
root.title("Image Encryption and Decryption")
root.geometry("650x540")
root.resizable(False, False)

root.configure(bg='#424952')
style = ttk.Style()
style.map('TCombobox', 
              selectbackground=[('readonly', 'white')],
              selectforeground=[('readonly', 'black')],
              background=[('readonly', 'white')],
              foreground=[('readonly', 'black')])

# Buttons Styling 
button_font_browser = font.Font(size=7)
button_font_transform = font.Font(size=10, weight="bold")

file_frame = tk.Frame(root, bg='#424952')
file_frame.pack()

path_label = tk.Label(file_frame, text="File", bg='#424952', fg='white')
path_label.pack(side="left", pady=15, padx=5)

path_entry = Entry(file_frame, width=50)
path_entry.pack(side="left", pady=15)

browse_button = tk.Button(file_frame, text="Browse", command=browse_image, bd=0, relief=tk.FLAT, font=button_font_browser)
browse_button.pack(side="left", pady=15, padx=5)

mode_frame = tk.Frame(root, bg='#424952')
mode_frame.pack(pady=10)

mode_label = tk.Label(mode_frame, text="Mode", bg='#424952', fg='white')
mode_label.pack(side="left", padx=8)

modes = ["Encryption", "Decryption"]
mode_var = tk.StringVar(root)
mode_var.set(modes[0]) 
mode_menu = ttk.Combobox(mode_frame, textvariable=mode_var, values=modes, width=10 ,state='readonly')
mode_menu.pack(side="left")

transform_button = tk.Button(root, text="Transform", command=transform_image, width=15, height=1, bd=0, bg='lime green')
transform_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset", command=reset, width=15, height=1, bd=0)
reset_button.pack(pady=5)

save_button = tk.Button(root, text="Save", command=save_image, width=15, height=1, bd=0)
save_button.pack(pady=5)

# Frame for image labels and panels
image_frame = tk.Frame(root, bg='#424952')
image_frame.pack(pady=5)

# labels for image areas
original_image_label = tk.Label(image_frame, text="Original Image", bg='#424952', fg='white')
original_image_label.pack(side="left", padx=(0, 100))

processed_image_label = tk.Label(image_frame, text="Processed Image", bg='#424952', fg='white')
processed_image_label.pack(side="right",padx=(100, 0))

# Placeholder labels
panelA_placeholder = tk.Label(root, text="Original Image Area", bg="grey", width=30, height=15, fg='white')
panelA_placeholder.pack(side="left", padx=40, pady=15)
panelA_placeholder.pack_propagate(False)

panelB_placeholder = tk.Label(root, text="Processed Image Area", bg="grey", width=30, height=15, fg='white')
panelB_placeholder.pack(side="right", padx=40, pady=15)
panelB_placeholder.pack_propagate(False)

# Start the GUI
root.mainloop()
