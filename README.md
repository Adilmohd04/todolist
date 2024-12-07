### Steps to Set Up the Project

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
   pytest todo/tests_integration.py
   ```

3. **Run End-to-End (E2E) Tests**
   Follow the Cypress setup steps and run tests using the Cypress UI.

---

### API Endpoints
The API supports the following operations:
- **GET** `/tasks/`: List all tasks
- **POST** `/tasks/`: Create a new task
- **PUT** `/tasks/<id>/`: Update a task
- **DELETE** `/tasks/<id>/`: Delete a task

Use tools like [Postman](https://www.postman.com/) to interact with the API.

---

### Contributing
Feel free to open issues or submit pull requests for improvements. Follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Feature description"`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

### License
This project is licensed under the [MIT License](LICENSE).

---

Let me know if you need more details or customizations!
