# Resonator

Resonator is a Flask-based note-taking web application built for CS50x 2026. It lets each user create an account, 
log in securely, and manage a personal collection of notes with Markdown formatting and tags. The application is intentionally small, but it still covers the full lifecycle of a practical CRUD app: authentication, ownership checks, searchable content, tagged organization, and a polished browser-based editor.

The core idea behind Resonator was to keep the product lightweight without making it feel barebones. Notes are stored in a local SQLite database through SQLAlchemy, while the UI is rendered with server-side templates so the app remains straightforward to understand and easy to deploy. Markdown support is handled in the browser with EasyMDE, which gives the editing experience a much more usable feel than a plain `<textarea>` while still storing simple text in the database.

## What the app does

After visiting the home page, a user can register, log in, and reach a dashboard that lists their notes. From there they can create a new note, edit an existing one, delete a note, search by title or body text, and filter by tag. Notes are private to the signed-in user; the application checks ownership before allowing edits or deletes. Tags are entered as comma-separated values and are normalized so repeated labels are not duplicated unnecessarily.

The interface is built around a shared base layout and a few focused pages: a landing page, login and registration forms, a dashboard, and a note editor. That structure keeps the code easy to navigate and lets the project stay visually consistent without repeating the same header, footer, and stylesheet references across multiple files.

## Running the project

### Prerequisites

- Python 3.13 or newer
- `pip`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/cs50/resonator.git
   cd resonator
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows, activate with:
   ```bash
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   flask run
   ```
5. Open `http://localhost:5000` in your browser.