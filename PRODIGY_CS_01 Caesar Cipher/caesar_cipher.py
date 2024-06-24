import string
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font

# Caesar Cipher Function
def caesar_cipher(text, shift, alphabets, mode):
    def shift_alphabet(alphabet, shift):
        return alphabet[shift % len(alphabet):] + alphabet[:shift % len(alphabet)]
    
    shift = shift if mode == "Encryption" else -shift
    shifted_alphabets = tuple(map(lambda alpha: shift_alphabet(alpha, shift), alphabets))
    final_alphabet = ''.join(alphabets)
    final_shifted_alphabet = ''.join(shifted_alphabets)
    table = str.maketrans(final_alphabet, final_shifted_alphabet)
    return text.translate(table)

# Get Output File Path Function
def get_output_file_path():
    return filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save the output file"
    )

# Transform Function 
def transform_text():
    text = input_text.get("1.0", tk.END).strip()
    file_path = file_entry.get().strip()
    
    if not text and not file_path:
        messagebox.showerror("Error", "Please provide input text or select an input file.")
        return
    
    if file_path and not text:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
    
    shift = int(shift_entry.get())
    mode = mode_var.get()
    alphabets = []
    if lowercase_var.get():
        alphabets.append(string.ascii_lowercase)
    if uppercase_var.get():
        alphabets.append(string.ascii_uppercase)
    if digits_var.get():
        alphabets.append(string.digits)
    if not alphabets:
        alphabets = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    
    result = caesar_cipher(text, shift, alphabets, mode)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    
    if file_path:
        output_file_path = get_output_file_path()
        if output_file_path:
            save_output(result, output_file_path)

# Select File Function
def select_file():
    filetypes = [("Text files", "*.txt"), 
                 ("Word documents", "*.docx"), 
                 ("Rich Text Format", "*.rtf"),
                 ("Word documents", "*.doc")]
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file_content)

# Save Output Function 
def save_output(output_text, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write(output_text)
    messagebox.showinfo("Success", f"Output saved to {output_file_path}")

#  GUI window
root = tk.Tk()
root.title("Caesar Cipher")
root.geometry("600x720")
root.resizable(False, False)

root.configure(bg='#424952')
style = ttk.Style()
    
# Customization in combobox 
style.map('TCombobox', 
           selectbackground=[('readonly', 'white')],
           selectforeground=[('readonly', 'black')],
           background=[('readonly', 'white')],
           foreground=[('readonly', 'black')])

# Customization in Buttons
button_font_browser = font.Font(size=7)
button_font_transform = font.Font(size=10,font=("Helvetica",12,'bold'), weight="bold")

# File Input
file_frame = tk.Frame(root, bg='#424952')
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="File", bg='#424952', fg='white')
file_label.grid(row=0, column=0, padx=5)

file_entry = tk.Entry(file_frame, width=40)
file_entry.grid(row=0, column=1, padx=5)

file_button = tk.Button(file_frame, text="Browse", command=select_file, bd=0, relief=tk.FLAT, font=button_font_browser)
file_button.grid(row=0, column=2, padx=5)

# Input Box 
input_label = tk.Label(root, text="Input", bg='#424952', fg='white')
input_label.pack(pady=(10, 0), padx=(0, 500))

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

input_scrollbar = tk.Scrollbar(input_frame)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

input_text = tk.Text(input_frame, height=10, wrap=tk.WORD, yscrollcommand=input_scrollbar.set)
input_text.pack(fill=tk.BOTH, expand=True)

input_scrollbar.config(command=input_text.yview)

# Mode & Shift
mode_shift_frame = tk.Frame(root, bg='#424952')
mode_shift_frame.pack(pady=5)

mode_label = tk.Label(mode_shift_frame, text="Mode", bg='#424952', fg='white')
mode_label.grid(row=0, column=0, padx=5)

mode_var = tk.StringVar(value="Encryption")
mode_menu = ttk.Combobox(mode_shift_frame, textvariable=mode_var, values=["Encryption", "Decryption"], state='readonly')
mode_menu.grid(row=0, column=1, padx=5)

shift_label = tk.Label(mode_shift_frame, text="Shift", bg='#424952', fg='white')
shift_label.grid(row=0, column=2, padx=5)
shift_entry = tk.Entry(mode_shift_frame, width=5)
shift_entry.insert(0, "13")
shift_entry.grid(row=0, column=3, padx=5, pady=10)

# Check-box
lowercase_var = tk.BooleanVar(value=True)
uppercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()

lowercase_check = tk.Checkbutton(root, text="Lowercase (abcdefghijklmnopqrstuvwxyz)", variable=lowercase_var, bg='#424952',font=("Helvetica",9), fg='white', selectcolor='#424952')
uppercase_check = tk.Checkbutton(root, text="Uppercase (ABCDEFGHIJKLMNOPQRSTUVWXYZ)", variable=uppercase_var, bg='#424952',font=("Helvetica",9), fg='white', selectcolor='#424952')
digits_check = tk.Checkbutton(root, text="Digits (0123456789)", variable=digits_var, bg='#424952', fg='white',font=("Helvetica",9), selectcolor='#424952')

lowercase_check.pack(padx=(0, 50)) 
uppercase_check.pack(padx=(0, 0)) 
digits_check.pack(padx=(0, 165))  

# Output 
output_label = tk.Label(root, text="Output", bg='#424952', fg='white')
output_label.pack(pady=(10, 0), padx=(0, 500))

output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

output_scrollbar = tk.Scrollbar(output_frame)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_frame, height=10, wrap=tk.WORD, yscrollcommand=output_scrollbar.set)
output_text.pack(fill=tk.BOTH, expand=True)

output_scrollbar.config(command=output_text.yview)

# Transform button
transform_button = tk.Button(root, text="Transform !!!", command=transform_text, bg='lime green', width=14, height=2, bd=0, relief=tk.FLAT, font=button_font_transform)
transform_button.pack(pady=15, padx=20)

root.mainloop()
