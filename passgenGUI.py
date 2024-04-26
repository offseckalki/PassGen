import tkinter as tk
import tkinter.messagebox as messagebox
import hashlib
import sqlite3
import secrets
import string

# Initialize SQLite database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create table to store passwords
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              service TEXT,
              password_hash TEXT,
              hint TEXT)''')
conn.commit()

def generate_memorable_password():
    # Define word lists for password generation
    word_list = ['apple', 'banana', 'orange', 'cherry', 'grape', 'lemon', 'lime', 'melon', 'kiwi', 'pear']
    password_length = 12  # Total number of characters in the password

    # Generate a memorable password by randomly selecting words
    password = '-'.join(secrets.choice(word_list) for _ in range(password_length // 3))  # Example: "banana-melon-cherry"
    return password

def hash_password(password):
    # Hash the password using SHA-256
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

def store_password(service, password, hint):
    # Generate password and hash
    hashed_password = hash_password(password)
    
    # Store in SQLite database with associated service and hint
    c.execute('''INSERT INTO passwords (service, password_hash, hint)
                 VALUES (?, ?, ?)''', (service, hashed_password, hint))
    conn.commit()

def get_hint_for_service(service_name):
    # Retrieve hint for the specified service from the database
    c.execute('''SELECT hint FROM passwords WHERE service = ?''', (service_name,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

def verify_password(service, guessed_password):
    # Retrieve stored hashed password for the specified service
    c.execute('''SELECT password_hash FROM passwords WHERE service = ?''', (service,))
    result = c.fetchone()
    if result:
        stored_password_hash = result[0]
        guessed_password_hash = hash_password(guessed_password)
        return guessed_password_hash == stored_password_hash
    else:
        return False

def on_store_password():
    service = entry_service.get()
    password = entry_password.get()
    hint = entry_hint.get()
    
    if service and password:
        store_password(service, password, hint)
        messagebox.showinfo("Password Manager", "Password stored successfully!")
        entry_service.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_hint.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Service and Password fields are required.")

def on_retrieve_hint():
    service_name = entry_service.get()
    if service_name:
        hint = get_hint_for_service(service_name)
        if hint:
            messagebox.showinfo("Hint", f"The hint for {service_name} is: {hint}")
        else:
            messagebox.showwarning("No Hint", f"No hint found for {service_name}.")
    else:
        messagebox.showerror("Error", "Service field is required.")

def on_verify_password():
    service_name = entry_service.get()
    guessed_password = entry_password.get()
    
    if service_name and guessed_password:
        if verify_password(service_name, guessed_password):
            messagebox.showinfo("Password Verification", "Password verified successfully!")
        else:
            messagebox.showerror("Password Verification", "Incorrect password. Please try again.")
    else:
        messagebox.showerror("Error", "Service and Password fields are required.")

# Create GUI window
root = tk.Tk()
root.title("Password Manager")

# Service Label and Entry
label_service = tk.Label(root, text="Service:")
label_service.pack()
entry_service = tk.Entry(root)
entry_service.pack()

# Password Label and Entry
label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Hint Label and Entry
label_hint = tk.Label(root, text="Hint:")
label_hint.pack()
entry_hint = tk.Entry(root)
entry_hint.pack()

# Buttons
button_store = tk.Button(root, text="Store Password", command=on_store_password)
button_store.pack(pady=10)

button_retrieve_hint = tk.Button(root, text="Retrieve Hint", command=on_retrieve_hint)
button_retrieve_hint.pack(pady=10)

button_verify_password = tk.Button(root, text="Verify Password", command=on_verify_password)
button_verify_password.pack(pady=10)

# Run the main event loop
root.mainloop()

# Close the database connection
conn.close()
