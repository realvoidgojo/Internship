import re
import tkinter as tk
from tkinter import ttk

def password_strength(password):
    length = len(password)
    score = length * 4

    uppercase_letters = len(re.findall(r'[A-Z]', password))
    lowercase_letters = len(re.findall(r'[a-z]', password))
    digits = len(re.findall(r'[0-9]', password))
    symbols = len(re.findall(r'[@$!%*?&#]', password))
    middle_digits_or_symbols = len(re.findall(r'(?<!^)[0-9@$!%*?&#](?!$)', password))

    score += ((length - uppercase_letters) + (length - lowercase_letters)) * 2 
    score += digits * 4 + symbols * 6 + middle_digits_or_symbols * 2
    
    req = sum([length >= 8, uppercase_letters > 0, lowercase_letters > 0, digits > 0, symbols > 0])
    if req >= 3:
        score += req * 2

    if re.fullmatch(r'[a-zA-Z]+', password) or re.fullmatch(r'\d+', password):
        score -= length
    
    repeat_chars = len(password) - len(set(password.lower()))
    consecutive_uppercase = len(re.findall(r'[A-Z]{2,}', password))
    consecutive_lowercase = len(re.findall(r'[a-z]{2,}', password))
    consecutive_digits = len(re.findall(r'[0-9]{2,}', password))
    
    sequential_patterns = [
        r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
        r'(?:012|123|234|345|456|567|678|789)',  # Sequential digits
        r'(?:@!#|!\$#|#\$%|\$%^|%^&|\^&\*|&\*\?|!\?#)'  # Sequential symbols
    ]

    sequential_deductions = sum(len(re.findall(pat, password.lower())) for pat in sequential_patterns)

    score -= (repeat_chars * 1.5 + consecutive_uppercase * 2 + consecutive_lowercase * 2 + consecutive_digits * 2 + sequential_deductions * 3)
    return max(0, min(score, 100))

def evaluate_strength(score):
    return ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][(score >= 20) + (score >= 40) + (score >= 60) + (score >= 80)]

def time_to_crack(password):
    charsets = [
        (r'[a-z]', 26),  # Lowercase letters
        (r'[A-Z]', 26),  # Uppercase letters
        (r'[0-9]', 10),  # Digits
        (r'[@$!%*?&#]', 32)  # All symbols
    ]
    
    charset_size = sum(size for pattern, size in charsets if re.search(pattern, password))
    combinations = charset_size ** len(password)
    
    attempts_per_second = 1_000_000_000  # Example: 1 billion attempts per second
    seconds_to_crack = combinations / attempts_per_second
    
    return seconds_to_crack

def format_time(seconds):
    intervals = (
        ('years', 31536000),  # 60 * 60 * 24 * 365
        ('days', 86400),       # 60 * 60 * 24
        ('hours', 3600),       # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            return f"{value:.0f} {name}"
    return "0 seconds"

def update_password_strength(event=None):
    password = password_var.get()
    score = password_strength(password)
    strength = evaluate_strength(score)
    time_to_crack_seconds = time_to_crack(password)
    time_to_crack_str = format_time(time_to_crack_seconds)

    strength_var.set(f"Password Strength: {strength}")
    time_var.set(f"Estimated Time to Crack: {time_to_crack_str}")
    progress_var.set(score)
    percentage_var.set(f"{score}%")

def toggle_password_visibility():
    if hide_password_var.get():
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

def clear_fields():
    password_var.set("")
    strength_var.set("Password Strength: ")
    time_var.set("Estimated Time to Crack: ")
    progress_var.set(0)
    percentage_var.set("0.0%")

root = tk.Tk()
root.title("Password Strength Meter")
root.geometry("600x350")
root.resizable(False, False)
root.configure(bg='#424952')



# Variables
password_var = tk.StringVar()
hide_password_var = tk.BooleanVar()
strength_var = tk.StringVar(value="Password Strength: ")
time_var = tk.StringVar(value="Estimated Time to Crack: ")
progress_var = tk.DoubleVar(value=0)
percentage_var = tk.StringVar(value="0.0%")

# Title
title_label = tk.Label(root, text="Password Strength Meter", font=("Helvetica", 16) ,bg='#424952', fg='white', justify='center')
title_label.pack(pady=10)

# Password Entry
password_entry = tk.Entry(root, textvariable=password_var, font=("Helvetica", 12), show="" , bd=0 ,width=32 ,justify='center')
password_entry.pack(pady=20,)
password_entry.bind("<KeyRelease>", update_password_strength)


# Hide Password Checkbox
hide_password_checkbox = tk.Checkbutton(root, text="Hide Password", variable=hide_password_var, command=toggle_password_visibility , bg='#424952', fg='white', selectcolor='#424952')
hide_password_checkbox.pack(padx=(0, 180),pady=3)

# Progress Bar
progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var, length=300)
progress_bar.pack(pady=10)

# Score Percentage
score_percentage_label = tk.Label(root, textvariable=percentage_var, font=("Helvetica", 12),bg='#424952', fg='white')
score_percentage_label.pack(pady=5)

# Password Strength
password_strength_label = tk.Label(root, textvariable=strength_var, font=("Helvetica", 12),bg='#424952', fg='white')
password_strength_label.pack(pady=5)

# Estimated Time to Crack
time_to_crack_label = tk.Label(root, textvariable=time_var, font=("Helvetica", 12),bg='#424952', fg='white')
time_to_crack_label.pack(pady=5)

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_fields , bg='lime green', bd=0 , relief=tk.FLAT , width=10)
clear_button.pack(pady=10)

root.mainloop()
