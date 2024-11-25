import tkinter as tk
from tkinter import messagebox
import random

# Initialize main window
root = tk.Tk()
root.title("RSA-Based Cryptomessenger")
root.geometry("1080x720")  # Full-screen resolution
root.configure(bg="black")

# Canvas for the outer Matrix effect
canvas = tk.Canvas(root, bg="black", width=1080, height=720, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Full background

# Matrix effect function for the border area
def create_matrix_effect():
    canvas.delete("matrix")  # Clear previous characters, but only those with tag 'matrix'

    # Generate Matrix-like characters in the border area only
    for _ in range(100):  # Density of characters in the border area
        x = random.choice(range(0, 150)) + random.choice([0, 900])
        y = random.randint(0, 720)
        binary_digit = random.choice(["0", "1"])
        canvas.create_text(x, y, text=binary_digit, fill="#00FF00", font=("Courier", 14), tags="matrix")
        
        x = random.randint(0, 1080)
        y = random.choice(range(0, 150)) + random.choice([0, 570])
        binary_digit = random.choice(["0", "1"])
        canvas.create_text(x, y, text=binary_digit, fill="#00FF00", font=("Courier", 14), tags="matrix")

    root.after(200, create_matrix_effect)  # Slower refresh effect by increasing interval

# Start the Matrix effect
create_matrix_effect()

# Add a title and the main bordered content area
title_label = tk.Label(root, text="Cryptomessenger by D & G", fg="white", bg="black", font=("Helvetica", 20, "bold"))
title_label.place(x=540, y=40, anchor="center")  # Centered title

# Outer white-bordered frame that wraps content
border_frame = tk.Frame(root, bg="white", width=860, height=580)
border_frame.place(relx=0.5, rely=0.5, anchor="center")

# Inner black frame within the border to hold all content
content_frame = tk.Frame(border_frame, bg="black")
content_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Contact Registration Section
tk.Label(content_frame, text="Register New Contact", fg="green", bg="black", font=("Helvetica", 12)).pack(pady=5)
contact_entry = tk.Entry(content_frame, width=40, bg="black", fg="green", insertbackground="green")
contact_entry.pack()
tk.Button(content_frame, text="Register Contact", command=lambda: register_contact(), bg="black", fg="green").pack(pady=5)

# Placeholder for dynamic user loading, replace with actual backend data
def load_contacts():
    return ["Alice", "Bob"]

# User selection dropdown and status indicator
tk.Label(content_frame, text="Select User to Message", fg="green", bg="black", font=("Helvetica", 12)).pack(pady=5)
user_selection = tk.StringVar(content_frame)
user_selection.set("Select a User")  # Default placeholder
user_menu = tk.OptionMenu(content_frame, user_selection, *load_contacts())
user_menu.config(bg="black", fg="green")
user_menu.pack()

# Status label
status_label = tk.Label(content_frame, text="Status: Unknown", fg="green", bg="black", font=("Helvetica", 12))
status_label.pack(pady=5)

# Update status label based on contact selection
def update_status():
    contact = user_selection.get()
    # Example placeholder: Fetch actual status from backend
    status = "Online" if contact == "Alice" else "Offline"  # Example logic
    status_label.config(text=f"Status: {status}")

user_selection.trace("w", lambda *args: update_status())  # Update status on selection change

# Chat History Section with increased width
chat_history = tk.Listbox(content_frame, width=80, height=12, bg="black", fg="green")
chat_history.pack(pady=5)

def add_message_to_history(message):
    chat_history.insert(tk.END, message)
    chat_history.yview(tk.END)  # Auto-scroll to the latest message

# Message Sent Confirmation Label
message_sent_label = tk.Label(content_frame, text="", fg="green", bg="black", font=("Helvetica", 12))
message_sent_label.pack(pady=5)

# Message Entry
tk.Label(content_frame, text="Enter Message", fg="green", bg="black", font=("Helvetica", 12)).pack(pady=5)
message_entry = tk.Entry(content_frame, width=40, bg="black", fg="green", insertbackground="green")
message_entry.pack()

# Preview Encryption Button
def preview_encryption():
    message = message_entry.get()
    if message:
        encrypted_message = message[::-1]  # Placeholder for actual encryption
        messagebox.showinfo("Preview Encrypted Message", f"Encrypted: {encrypted_message}")
    else:
        messagebox.showerror("Error", "Enter a message to encrypt.")

tk.Button(content_frame, text="Preview Encryption", command=preview_encryption, bg="black", fg="green").pack(pady=5)

# Define Register Contact function
def register_contact():
    contact_name = contact_entry.get()
    if contact_name:
        messagebox.showinfo("Contact Registered", f"{contact_name} has been registered.")
    else:
        messagebox.showerror("Error", "Enter a valid contact name.")

# Define Send Message function
def send_message():
    recipient = user_selection.get()
    message = message_entry.get()
    if recipient and message:
        encrypted_message = message[::-1]  # Placeholder for encrypted message
        add_message_to_history(f"You to {recipient}: {message}")
        message_sent_label.config(text=f"Message Sent to {recipient}")  # Display confirmation
    else:
        messagebox.showerror("Error", "Select a user and enter a message.")

# Send Message Button
tk.Button(content_frame, text="Send Message", command=send_message, bg="black", fg="green").pack(pady=5)

root.mainloop()
