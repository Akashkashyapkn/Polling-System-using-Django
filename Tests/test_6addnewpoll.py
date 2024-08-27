import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TestAddnewpoll:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        logger.info("WebDriver initialized")
  
    def teardown_method(self, method):
        self.driver.quit()
        logger.info("WebDriver closed")
  
    def test_addnewpoll(self):
        try:
            self.driver.get("http://127.0.0.1:8000/")
            self.driver.set_window_size(1050, 708)
            logger.info("Navigated to the homepage")
            self.perform_login("admin", "admin@123")
            logger.info("Logged in as 'admin'")
            self.add_new_poll("new", "a", "b")
            logger.info("New poll added successfully")
            self.logout()
            logger.info("Logged out successfully")
            assert "Get Started !" in self.driver.page_source, "Homepage not found after logout"
            logger.info("User is back on the homepage")

        except TimeoutException as e:
            logger.error(f"TimeoutException: {e}")
            self.driver.save_screenshot('screenshot.png')
            raise
        except Exception as e:
            logger.error(f"Exception: {e}")
            self.driver.save_screenshot('screenshot.png')
            raise

    def perform_login(self, username, password):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Get Started !"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

    def add_new_poll(self, poll_text, choice1, choice2):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Add"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_text"))
        ).send_keys(poll_text)
        self.driver.find_element(By.ID, "id_choice1").send_keys(choice1)
        self.driver.find_element(By.ID, "id_choice2").send_keys(choice2)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

    def logout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Get Started !"))
        )

if __name__ == "__main__":
    result = pytest.main(["-v", "--tb=short", "--maxfail=1"])
    if result == 0:
        logger.info("Test passed successfully.")
    else:
        logger.error("Test failed.")