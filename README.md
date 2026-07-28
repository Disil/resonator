# Resonator

Resonator is a Flask-based note-taking web application built for CS50x 2026. It lets each user create an account, log in securely, and manage a personal collection of notes with markdown formatting and tags. The application is intentionally small, but it still covers the full lifecycle of a practical CRUD app: authentication, ownership checks, searchable content, tagged organization, and a polished browser-based editor.

The core idea behind Resonator was to keep the product lightweight without making it feel barebones. Notes are stored in a local SQLite database through SQLAlchemy, while the UI is rendered with server-side templates so the app remains straightforward to understand and easy to deploy. Markdown support is handled in the browser with EasyMDE, which gives the editing experience a much more usable feel than a plain `<textarea>` while still storing simple text in the database.

## What the app does

After visiting the home page, a user can register, log in, and reach a dashboard that lists their notes. From there they can create a new note, edit an existing one, delete a note, search by title or body text, and filter by tag. Notes are private to the signed-in user; the application checks ownership before allowing edits or deletes. Tags are entered as comma-separated values and are normalized so repeated labels are not duplicated unnecessarily.

The interface is built around a shared base layout and a few focused pages: a landing page, login and registration forms, a dashboard, and a note editor. That structure keeps the code easy to navigate and lets the project stay visually consistent without repeating the same header, footer, and stylesheet references across multiple files.

## Project structure

Below is the file-by-file layout of the project and what each part does.

- `app.py` – The main Flask application. It configures the app, initializes the database, defines the authentication flow, and exposes all routes for the landing page, registration, login, logout, dashboard, note creation, note editing, and note deletion. It also includes helper functions for tag parsing and tag synchronization.
- `models.py` – The database layer. This file defines the `User`, `Note`, and `Tag` models, the many-to-many association table between notes and tags, password hashing helpers, and a `to_dict()` helper for serializing notes.
- `requirements.txt` – The Python dependencies needed to run the project: Flask, Flask-SQLAlchemy, SQLAlchemy, and Werkzeug.
- `templates/base.html` – The shared layout used by every page. It provides the navigation bar, the shared stylesheet links, the favicon, and the common content blocks for child templates.
- `templates/index.html` – The public landing page. It introduces the project and points users toward login or registration.
- `templates/login.html` – The login form. It accepts either a username or email address plus a password.
- `templates/register.html` – The registration form. It collects username, email, and password and creates a new user record.
- `templates/dashboard.html` – The authenticated notes overview. It shows note cards, search controls, tag filters, timestamps, and actions for editing or deleting notes.
- `templates/edit_note.html` – The note editor used for both creating and editing notes. It includes the EasyMDE markdown editor, tag input, validation for required content, and the submit/cancel controls.
- `static/easymde.min.css` and `static/easymde.min.js` – The bundled EasyMDE assets that power the markdown editor in the note form.
- `static/pico.conditional.green.css` – The Pico.css stylesheet used to give the app a clean, responsive baseline design.
- `static/favicon-32x32.png` – The browser favicon.
- `instance/database.db` – The SQLite database file created locally when the app runs. This is runtime data rather than source code, but it is part of the working project state.
- `instance/IMPLEMENTATION_NOTES.md` – Internal notes describing implementation details and project decisions.

## Design choices

Several implementation choices were made deliberately. First, the app uses SQLAlchemy relationships instead of storing tags as a plain comma-separated string in the note record. That decision makes filtering by tag much cleaner, avoids duplicated tag data, and keeps the data model flexible if the app grows later. The helper in `app.py` still accepts user-friendly comma-separated input, but the database stores tags in a normalized way.

Second, authentication is handled with server-side sessions and hashed passwords rather than storing anything sensitive in cookies or plain text. This keeps the security model simple while still following standard Flask practices. The app also checks note ownership before allowing edit or delete actions, which is important because each user should only manage their own data.

Third, the editor uses EasyMDE instead of a raw textarea because note-taking apps benefit from an immediate previewable markdown experience. That said, the content is still saved as plain markdown text, which keeps the backend portable and avoids locking the project into a specific rendering pipeline.

Finally, the UI uses Jinja template inheritance through `base.html`. I chose that pattern because it reduces duplication and makes it easier to adjust the global layout, navigation, or styling in one place. For a project of this size, that tradeoff keeps the code readable without adding unnecessary complexity.

## Running the project locally

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

If you prefer, you can also run the app directly with Python:

```bash
python app.py
```

## Usage notes

When a new visitor opens the site, they see the landing page and can choose to register or log in. Once authenticated, they are sent to the dashboard, where each note appears as a card with its title, a short preview, timestamps, and any associated tags. Clicking a tag filters the dashboard to notes with that label, and the search field can narrow results by title or content. Creating or editing a note opens the same editor, which keeps the interface consistent and minimizes duplicate code.

Resonator was built as a final project, but it is also a good foundation for future enhancements. Useful next steps would include full note detail pages, richer tag management, optional note pinning, or exporting notes as markdown or HTML. The current version keeps the scope focused so the core note workflow remains reliable and easy to understand.
