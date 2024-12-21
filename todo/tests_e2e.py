import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests

# Set up the WebDriver
service = Service(executable_path='todo/driver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Helper function for logging in
def login_admin():
    try:
        driver.get('http://127.0.0.1:8000/admin/')
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_field = driver.find_element(By.NAME, 'password')

        # Enter admin credentials
        username_field.send_keys('adil')
        password_field.send_keys('0004')
        password_field.send_keys(Keys.RETURN)  # Use Keys.RETURN to simulate pressing the Enter key
        print("Logged in as admin.")
        WebDriverWait(driver, 10).until(
            EC.url_to_be('http://127.0.0.1:8000/admin/')  # Wait until redirected back to the admin page
        )
    except Exception as e:
        print(f"Error during login: {e}")

# Function to get and store all task IDs
def get_task_ids():
    try:
        # Include username and password in the URL for basic authentication
        url = 'http://127.0.0.1:8000/tasks/'
        response = requests.get(url, auth=('adil', '0004'))  # Basic authentication with requests
        
        # Check if the response is valid
        if response.status_code == 200:
            tasks = response.json()  # Parse the JSON response
            if not tasks:
                print("No tasks available.")
                return []

            # Store task IDs in a list
            task_ids = [task.get('id') for task in tasks if task.get('id')]
            return task_ids
        else:
            print(f"Failed to retrieve tasks. HTTP Status Code: {response.status_code}")
            return []

    except Exception as e:
        print(f"Error during task ID retrieval: {e}")
        return []

# Function to create a task
def create_task():
    try:
        driver.get('http://127.0.0.1:8000/')

        # Locate and click "New Task" button
        new_task_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.new-task-btn'))
        )
        new_task_button.click()

        # Fill in the task form
        title_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'title'))
        )
        description_field = driver.find_element(By.NAME, 'description')
        due_date_field = driver.find_element(By.NAME, 'due_date')
        tags_field = driver.find_element(By.NAME, 'tags')
        status_field = driver.find_element(By.NAME, 'status')

        # Provide task details
        title_field.send_keys('Samfrople Task')
        description_field.send_keys('This is a sample task.')
        due_date_field.send_keys('2024-12-31')  # Adjusted the date format
        tags_field.send_keys('Urgent')
        status_field.send_keys('Completed')

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Wait for confirmation or task to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.task-container'))
        )
        print("Task created successfully.")

    except Exception as e:
        print(f"Error during task creation: {e}")

def update_task(task_id):
    try:
        driver.get(f'http://127.0.0.1:8000/form/{task_id}/')

        # Wait for the form fields to load
        title_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'title'))
        )
        description_field = driver.find_element(By.NAME, 'description')
        due_date_field = driver.find_element(By.NAME, 'due_date')
        tags_field = driver.find_element(By.NAME, 'tags')
        status_field = driver.find_element(By.NAME, 'status')

        # Update task details
        title_field.clear()
        title_field.send_keys('Updated Task Title')
        description_field.clear()
        description_field.send_keys('Updated task description.')
        due_date_field.clear()
        due_date_field.send_keys('2024-12-31')
        tags_field.clear()
        tags_field.send_keys('Updated,Important')
        status_field.send_keys('In Progress')

        # Submit the updated task
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Wait for confirmation
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.task-container'))
        )
        print(f"Task {task_id} updated successfully.")

    except Exception as e:
        print(f"Error during task update: {e}")


def delete_task(task_id):
    try:
        driver.get(f'http://127.0.0.1:8000/tasks/{task_id}/delete/')

        # Wait for the delete confirmation button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )

        # Click delete button
        delete_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        delete_button.click()

        # Wait for task deletion confirmation
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.task-container'))
        )
        print(f"Task {task_id} deleted successfully.")

    except Exception as e:
        print(f"Error during task deletion: {e}")

# Main function to execute the tests
def main():
    try:
        login_admin()
        create_task()  # Create a new task
        task_ids = get_task_ids()  # Get and store task IDs

        if not task_ids:
            print("No tasks available.")
            return

        # Select the last task
        task_id = task_ids[-1]
        print(f"Selected task ID: {task_id}")

        # View the task details
        url = f'http://127.0.0.1:8000/tasks/{task_id}/'
        response = requests.get(url, auth=('adil', '0004'))
        if response.status_code == 200:
            task = response.json()
            print(f"Viewing task {task_id}: {task}")
        else:
            print(f"Failed to view task {task_id}. HTTP Status Code: {response.status_code}")

        # Update the task
        update_task(task_id)

        # Delete the task
        delete_task(task_id)

    finally:
        # Close the browser after the test
        driver.quit()

if __name__ == '__main__':
    main()
