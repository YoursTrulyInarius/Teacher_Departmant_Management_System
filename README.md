# Teacher Management System (TMS)

A clean and intuitive desktop-based Teacher Management System built with Python and Tkinter. This application allows educational departments to manage teacher records efficiently with persistent SQLite storage.

## 🚀 Features

- **Teacher Records Management**: Full CRUD (Create, Read, Update, Delete) operations for teacher information.
- **Department Tracking**: Organize teachers by their respective departments.
- **Dynamic Search**: Real-time filtering of records by name, email, or department.
- **Modern UI**: A user-friendly interface using Tkinter's `ttk` and custom styling (optimized for 1100x650 resolution).
- **Persistent Storage**: Data is safely stored in a local SQLite database (`ims_records.db`).
- **Validation**: Basic form validation to ensure name integrity.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Database**: SQLite3

## 📂 Project Structure

- `main.py`: The main entry point of the application containing the GUI logic and Teacher Record form.
- `database.py`: Handles all database operations for the `teachers` table.
- `ims_records.db`: The SQLite database file (created automatically on first run).

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/teacher-management-system.git
   cd teacher-management-system
   ```

2. **Ensure Python is installed**:
   This project requires Python 3. Tkinter is usually included with standard Python installations.

## 🚀 Usage

Run the following command to start the application:

```bash
python main.py
```

Created By: Sonjeev C. Cabardo