# Webknot Assignment

A Django-based web application designed to manage user data efficiently.

## Tech Stack

- **Backend**: Django  
- **Frontend**: HTML, CSS  
- **Database**: SQLite (default)  
- **Environment Management**: Virtualenv
  
## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dj-ayush/Webknot-Assignment.git
   cd Webknot-Assignment
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Linux/Mac
   source venv/bin/activate  
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

   Access the application at:  
   `http://127.0.0.1:8000/`

## License
This project is licensed under the MIT License.
