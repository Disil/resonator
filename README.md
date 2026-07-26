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
   git clone
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