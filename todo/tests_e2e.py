from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--remote-debugging-port=9222")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)


def login_admin():
    try:
        driver.get("http://127.0.0.1:8000/admin/")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")

        username_field.send_keys("adil")
        password_field.send_keys("0004")
        password_field.send_keys(Keys.RETURN)
        print("Logged in as admin.")
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/admin/"))
    except Exception as e:
        print(f"Error during login: {e}")


def get_task_ids():
    try:
        url = "http://127.0.0.1:8000/tasks/"
        response = requests.get(url, auth=("adil", "0004"))
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                print("No tasks available.")
                return []
            task_ids = [task.get("id") for task in tasks if task.get("id")]
            return task_ids
        else:
            print(f"Failed to retrieve tasks. HTTP Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error during task ID retrieval: {e}")
        return []


def create_task():
    try:
        driver.get("http://127.0.0.1:8000/")
        new_task_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-task-btn"))
        )
        new_task_button.click()

        title_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        description_field = driver.find_element(By.NAME, "description")
        due_date_field = driver.find_element(By.NAME, "due_date")
        tags_field = driver.find_element(By.NAME, "tags")
        status_field = driver.find_element(By.NAME, "status")

        title_field.send_keys("Samfrople Task")
        description_field.send_keys("This is a sample task.")
        due_date_field.send_keys("2024-12-31")
        tags_field.send_keys("Urgent")
        status_field.send_keys("Completed")

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-container"))
        )
        print("Task created successfully.")
    except Exception as e:
        print(f"Error during task creation: {e}")


def update_task(task_id):
    try:
        driver.get(f"http://127.0.0.1:8000/form/{task_id}/")

        title_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        description_field = driver.find_element(By.NAME, "description")
        due_date_field = driver.find_element(By.NAME, "due_date")
        tags_field = driver.find_element(By.NAME, "tags")
        status_field = driver.find_element(By.NAME, "status")

        title_field.clear()
        title_field.send_keys("Updated Task Title")
        description_field.clear()
        description_field.send_keys("Updated task description.")
        due_date_field.clear()
        due_date_field.send_keys("2024-12-31")
        tags_field.clear()
        tags_field.send_keys("Updated,Important")
        status_field.send_keys("In Progress")

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-container"))
        )
        print(f"Task {task_id} updated successfully.")
    except Exception as e:
        print(f"Error during task update: {e}")


def delete_task(task_id):
    try:
        driver.get(f"http://127.0.0.1:8000/tasks/{task_id}/delete/")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )

        delete_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        delete_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-container"))
        )
        print(f"Task {task_id} deleted successfully.")
    except Exception as e:
        print(f"Error during task deletion: {e}")


def main():
    try:
        login_admin()
        create_task()
        task_ids = get_task_ids()

        if not task_ids:
            print("No tasks available.")
            return

        task_id = task_ids[-1]
        print(f"Selected task ID: {task_id}")

        url = f"http://127.0.0.1:8000/tasks/{task_id}/"
        response = requests.get(url, auth=("adil", "0004"))
        if response.status_code == 200:
            task = response.json()
            print(f"Viewing task {task_id}: {task}")
        else:
            print(
                f"Failed to view task {task_id}. HTTP Status Code: {response.status_code}"
            )

        update_task(task_id)
        delete_task(task_id)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
