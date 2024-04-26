import secrets
import string
import hashlib
import sqlite3
import getpass

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

def generate_complex_password():
    # Define character sets for password generation
    characters = string.ascii_letters + string.digits + string.punctuation  # Uppercase + Lowercase + Digits + Symbols
    password_length = 16  # Password length (adjust as needed)

    # Generate a strong password with random characters
    password = ''.join(secrets.choice(characters) for _ in range(password_length))
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

def get_user_password():
    print("\nEnter your own password:")
    service = input("Enter the name of the service: ")
    while True:
        password = getpass.getpass("Enter your password: ")
        confirm_password = getpass.getpass("Confirm your password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    hint = input("Enter a hint to remember your password: ")
    store_password(service, password, hint)
    print("Password stored successfully!")

def generate_password_with_help():
    print("\nGenerating password with predefined prompts:")
    service = input("Enter the name of the service: ")
    dob = input("Enter your date of birth (DDMMYYYY): ")
    vehicle_no = input("Enter your vehicle number: ")
    pet_name = input("Enter your pet's name: ")
    favorite_person = input("Enter the name of your favorite singer/actor/player: ")

    # Create password using predefined prompts
    password = f"{dob}-{vehicle_no}-{pet_name}-{favorite_person}"
    hint = "DOB,Vehcle No, Pet name- favourite person"
    
    store_password(service, password, hint)
    print(f"Generated password: {password}")
    print("Password stored successfully!")

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

def main():
    while True:
        print("\nWelcome to Password Manager!")
        print("1. Enter your own password")
        print("2. Generate memorable password")
        print("3. Find hint for the pass!")
        print("4. Verify password for a service")
        print("5. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            get_user_password()
        elif choice == '2':
            generate_password_with_help()
        elif choice == '3':
            service_name=input("Enter the name of the service to retrieve the pass ")
            hint= get_hint_for_service(service_name)
            if hint:
                print(f"The hint for the {service_name} is : {hint}")
                
            else:
                print(f"No hint found for {service_name}.")
        elif choice== '4':
            service_name = input("Enter the name of the service to verify the password: ")
            guessed_password = getpass.getpass("Enter your password to verify: ")
            if verify_password(service_name, guessed_password):
                print("Password verified successfully!")
            else:
                print("Incorrect password. Please try again.")
        elif choice == '5':
            print("Thank you for using Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
