# Resonator
A note-taking web application built with Flask and SQLAlchemy, featuring a markdown editor. Created for the final project of CS50x 2026.

## Features
- Create, read, update, and delete notes (CRUD functionality)
- Markdown support for rich text formatting
- Tag notes with comma-separated labels and filter by tag
- Responsive design, based on Pico.css

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- ORM: SQLAlchemy
- Frontend: HTML/CSS (Pico CSS)
- Markdown Editor: EasyMDE

## Installation

### Prerequisites
- Python 3.13
- pip

### Setup
1. Clone the repository: 
   ```bash
   git clone https://github.com/cs50/resonator.git
2. Navigate to the project directory:
   ```bash
   cd resonator
3. Create a virtual environment:
   ```bash
   python -m venv venv
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
    - On macOS/Linux:
      ```bash
        source venv/bin/activate
        ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
6. Run the application:
   ```bash
   flask run
7. Open your web browser and go to `http://localhost:5000` to access the application.
   
## Usage
### Flow
When user first visited the website, they will be greeted with a welcome page from index.html. Then they can either create an account or log into an existing account. They can then navigate to the notes page to create, view, edit, and delete notes. Users can also tag their notes and filter them by tags.
### Structure
This is the folder structure of the project:
```
resonator/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── notes.html
│   ├── dashboard.html
│   ├── edit_note.html
│   └── base.html
├── static/
│   ├── easymde css and js files
│   └── favicon.ico
├── app.py
├── models.py
├── requirements.txt