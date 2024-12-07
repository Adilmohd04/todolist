Hosted Link
Access the live version of the To-Do List application here:
🔗 https://adil001.pythonanywhere.com/


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

### Cypress Setup (E2E Testing)

1. **Navigate to Cypress Directory**
   ```bash
   cd todo/cypress
   ```

2. **Install Cypress Dependencies**
   Use `npm` to install the required Node.js modules.
   ```bash
   npm install
   ```

3. **Run Cypress Tests**
   Launch Cypress to run the end-to-end tests.
   ```bash
   npx cypress open
   ```

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
   Follow the Cypress setup steps and run tests using the Cypress UI.
 ```bash
   cd todo/cypress
   npm install cypress
   npm cypress run
   ```
---

### API Endpoints
TSet Base URL: Use an environment variable, e.g., {{baseUrl}}.

Base URL: https://adil001.pythonanywhere.com
Add Requests: Create the following 5 requests in the collection:

GET /tasks/: Fetch all tasks.
POST /tasks/: Add a new task (include JSON body).
GET /tasks/{id}/: Fetch task by ID.
PUT /tasks/{id}/: Update task by ID (include JSON body).
DELETE /tasks/{id}/: Delete task by ID.
Export the Collection:

Click the collection's menu (three dots) → Export → Save as JSON.
Test the APIs:

Ensure each request works with the live Django app.

