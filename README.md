
# To-Do List Application

Access the live version of the To-Do List application here:  
🔗 [https://adil001.pythonanywhere.com/](https://adil001.pythonanywhere.com/)

---

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Adilmohd04/todolist.git
   cd todolist
   ```

2. **Set Up a Virtual Environment**
   Create and activate a virtual environment to isolate dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Backend Dependencies**
   Install all required Python libraries.
   ```bash
   pip install -r requirements.txt
   pip install django djangorestframework
   pip install djangorestframework-simplejwt
   pip install flake8 black
   ```

4. **Run Database Migrations**
   Apply migrations to set up the database.
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   Start the Django server to test the backend.
   ```bash
   python manage.py runserver
   ```

   The server will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### Selenium Setup (E2E Testing)

1. **Install Selenium and WebDriver Manager**
   Install the necessary dependencies for running Selenium tests.
   ```bash
   pip install selenium webdriver-manager
   ```

2. **Run Selenium Tests**
   Execute the Selenium-based E2E tests:
   ```bash
   python todo/tests_e2e.py
   ```

   This will run your end-to-end tests using Selenium.

---

### Running Linting Tools

1. **Check Code Style with Flake8**
   ```bash
   flake8
   ```

2. **Format Code with Black**
   ```bash
   black .
   ```

---

### Running Automated Tests

1. **Run Unit Tests**
   ```bash
   python manage.py test
   ```

2. **Run Integration Tests**
   ```bash
   python todo/tests_integration.py
   ```

3. **Run End-to-End (E2E) Tests**
   Follow the Selenium setup steps and run tests with the following command:
   ```bash
   python todo/tests_e2e.py
   ```

---

### API Endpoints
Test Base URL: Use an environment variable, e.g., `{{baseUrl}}`.

**Base URL:** [https://adil001.pythonanywhere.com](https://adil001.pythonanywhere.com)

**Add Requests:** Create the following 5 requests in the collection:
```bash
{
  "title": "icecream",
  "description": "Milk, Bread, Eggs",
  "due_date": "2024-12-10",
  "tags": ["tag1"],
  "status": "OPEN"
}
```

**API Endpoints:**

- **GET /tasks/**: Fetch all tasks.
- **POST /tasks/**: Add a new task (include JSON body).
- **GET /tasks/{id}/**: Fetch task by ID.
- **PUT /tasks/{id}/**: Update task by ID (include JSON body).
- **DELETE /tasks/{id}/**: Delete task by ID.

---

This setup replaces Cypress with Selenium for end-to-end testing. Let me know if you need further modifications!
