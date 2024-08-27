import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TestAdminlogin():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        logger.info("Setup WebDriver")
  
    def teardown_method(self, method):
        self.driver.quit()
        logger.info("Teardown WebDriver")
  
    def test_adminlogin(self):
        try:
            self.driver.get("http://127.0.0.1:8000/")
            self.driver.set_window_size(784, 728)
            self.driver.find_element(By.LINK_TEXT, "Get Started !").click()
            logger.info("Navigated to Get Started page")
            
            self.driver.find_element(By.NAME, "username").send_keys("admin")
            self.driver.find_element(By.NAME, "password").send_keys("admin@123")
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
            logger.info("Admin credentials entered and login button clicked")
    
            logout_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
            )
            assert logout_link.is_displayed(), "Logout link should be visible after admin login"
            logger.info("Admin login successful, Logout link found")
    
           
            logout_link.click()
            logger.info("Admin logout successful")

          
            self.driver.find_element(By.LINK_TEXT, "Get Started !").click()
            self.driver.find_element(By.NAME, "username").send_keys("Akash")
            self.driver.find_element(By.NAME, "password").send_keys("Akash@45")
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
            logger.info("User credentials entered and login button clicked")

            logout_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
            )
            assert logout_link.is_displayed(), "Logout link should be visible after user login"
            logger.info("User login successful, Logout link found")

            logout_link.click()
            logger.info("User logout successful")

            assert True 

        except TimeoutException as e:
            logger.error(f"TimeoutException: {e}")
            self.driver.save_screenshot('screenshot.png')
            raise

if __name__ == "__main__":
    result = pytest.main(["-v", "--tb=short", "--maxfail=1"])
    if result == 0:
        print("Test passed successfully.")
    else:
        print("Test failed.")
