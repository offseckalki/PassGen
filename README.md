# Password Manager

This is a simple Password Manager application implemented in Python with a graphical user interface (GUI) using `tkinter`. It allows users to store, generate, retrieve hints, and verify passwords securely.

## Features

- **Store Passwords:** Store passwords securely in an SQLite database along with associated service names and hints.
- **Generate Passwords:** Generate memorable or complex passwords using predefined prompts or random characters.
- **Retrieve Hints:** Retrieve hints associated with stored passwords for specific services.
- **Verify Passwords:** Verify if a guessed password matches the stored password for a service.

## Requirements

- Python 3.x
- `tkinter` (included in standard Python library)
- SQLite3 (included in standard Python library)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/password-manager.git
    ```

2. Navigate to the project directory:
    ```bash
    cd password-manager
    ```

3. Run the application:
    ```bash
    python password_manager.py
    ```

## Usage

1. Launch the application by running `password_manager.py`.
2. Choose from the available options in the GUI:
   - **Enter your own password:** Manually input a service name, password, and hint to store in the database.
   - **Generate memorable password:** Generate a memorable password using predefined word prompts.
   - **Retrieve Hint:** Retrieve a hint associated with a specific service name.
   - **Verify password for a service:** Verify if a guessed password matches the stored password for a service.
   - **Exit:** Close the application.

## Screenshots

<https://github.com/offseckalki/PassGen/blob/main/ScreenShots/1.png?raw=true>
-->

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

---

For detailed usage instructions and additional information, refer to the [documentation](https://github.com/yourusername/password-manager).

If you encounter any issues or have questions, please open an [issue](https://github.com/yourusername/password-manager/issues).

Enjoy managing your passwords securely with this Password Manager!
