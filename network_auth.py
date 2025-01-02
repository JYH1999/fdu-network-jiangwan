import time
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='auto_login.log',
    filemode='a'
)

# Configuration
LOGIN_URL = 'http://10.102.250.36/#/login'
USERNAME = 'your_username'
PASSWORD = 'your_password'
LOGIN_BUTTON_XPATH = "/html/body/div/div/div/div[2]/div/div[3]/div[5]/div"
CHINESE_UNICOM_BUTTON_XPATH = "/html/body/div/div/div/div[2]/div/div[1]/div/div[5]/div"
LOGOUT_BUTTON_XPATH = "/html/body/div/div/div/div[2]/div/div[7]/div[2]"
AUTH_SUCCESS_XPATH = "//span[contains(text(), '认证成功')]"

def list_buttons(driver):
    """
    Find and print all clickable buttons on the current page.
    """
    logging.info("\nAll clickable buttons on the page:")
    buttons = []

    # Find all <button> tags
    buttons += driver.find_elements(By.TAG_NAME, 'button')

    # Find all elements with the 'sy-button' class
    buttons += driver.find_elements(By.CSS_SELECTOR, '.sy-button')

    # Find all elements with the 'el-button' class (if any)
    buttons += driver.find_elements(By.CSS_SELECTOR, '.el-button')

    # Add more selectors as needed

    # Remove duplicate elements
    unique_buttons = list(set(buttons))

    if not unique_buttons:
        logging.info("No buttons found on the page.")
        return []

    for index, button in enumerate(unique_buttons, start=1):
        try:
            # Get the visible text of the button
            text = button.text.strip()
            # Get the tag name
            tag_name = button.tag_name
            # Get the class name
            class_attr = button.get_attribute('class')
            # Get a part of the outer HTML for context
            outer_html = button.get_attribute('outerHTML')
            # Print button details
            logging.info(f"Button {index}:")
            logging.info(f"  Text: '{text}'")
            logging.info(f"  Tag: {tag_name}")
            logging.info(f"  Class: {class_attr}")
            logging.info(f"  Outer HTML: {outer_html[:100]}...")  # Print only the first 100 characters
            logging.info("-" * 40)
        except Exception as e:
            logging.error(f"Error getting details for button {index}: {e}")

    return unique_buttons

def check_auth_success(driver):
    """
    Check if the page contains the text "认证成功" (authentication success).
    Returns True if found, False otherwise.
    """
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, AUTH_SUCCESS_XPATH)))
        logging.info("Detected '认证成功' (authentication success).")
        return True
    except:
        logging.info("Did not detect '认证成功' (authentication success).")
        return False

def perform_logout(driver):
    """
    Perform the logout operation.
    """
    try:
        logging.info("Starting logout operation.")
        # Locate the logout button using the provided absolute XPath
        logout_button = driver.find_element(By.XPATH, LOGOUT_BUTTON_XPATH)
        # Log the button's properties for confirmation
        logging.info(f"Logout button text: '{logout_button.text}'")
        logging.info(f"Logout button class: {logout_button.get_attribute('class')}")
        # Scroll to the logout button to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)
        time.sleep(1)  # Wait for scroll to complete
        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", logout_button)
        logging.info("Clicked logout button.")
        # Wait for the page response after logout
        time.sleep(3)
        logging.info("Waited 3 seconds after clicking the logout button.")
        # Take a screenshot after clicking the logout button
        driver.save_screenshot("after_logout_click.png")
        logging.info("Saved screenshot after logout button click as after_logout_click.png")
    except Exception as e:
        logging.error(f"Unable to click logout button: {e}")
        # Take a screenshot for debugging
        driver.save_screenshot("logout_button_error.png")
        logging.info("Saved screenshot after logout button error as logout_button_error.png")
        raise e  # Reraise the exception

def perform_login(driver, username, password):
    """
    Perform the login operation.
    """
    try:
        # Step 1: Enter username
        try:
            username_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入用户名"]')
            username_input.clear()
            username_input.send_keys(username)
            logging.info("Username entered.")
        except Exception as e:
            logging.error(f"Unable to find username input field: {e}")
            driver.save_screenshot("username_input_error.png")
            logging.info("Saved screenshot after username input error as username_input_error.png")
            raise e

        # Step 2: Enter password
        try:
            password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
            password_input.clear()
            password_input.send_keys(password)
            logging.info("Password entered.")
        except Exception as e:
            logging.error(f"Unable to find password input field: {e}")
            driver.save_screenshot("password_input_error.png")
            logging.info("Saved screenshot after password input error as password_input_error.png")
            raise e

        # Step 3: Check "Roaming No Authentication" checkbox
        try:
            checkbox = driver.find_element(By.XPATH, "//span[text()='漫游免认证']/preceding-sibling::span[@class='el-checkbox__input']/input[@type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)  # Use JavaScript click to ensure the action is executed
            logging.info("Checked 'Roaming No Authentication' checkbox.")

            # Verify if the checkbox is checked
            is_checked = checkbox.is_selected()
            logging.info(f"Checkbox checked status: {is_checked}")
        except Exception as e:
            logging.error("Failed to check checkbox, trying to click label instead.")
            # Alternative method: Click the label containing "Roaming No Authentication"
            try:
                label = driver.find_element(By.XPATH, "//span[text()='漫游免认证']/..")
                label.click()
                logging.info("Clicked label to check 'Roaming No Authentication' checkbox.")

                # Verify if the checkbox is checked
                checkbox = driver.find_element(By.XPATH, "//span[text()='漫游免认证']/preceding-sibling::span[@class='el-checkbox__input']/input[@type='checkbox']")
                is_checked = checkbox.is_selected()
                logging.info(f"Checkbox checked status: {is_checked}")
            except Exception as inner_e:
                logging.error(f"Failed to click label for checkbox: {inner_e}")
                # Take a screenshot for debugging
                driver.save_screenshot("checkbox_error.png")
                logging.info("Saved screenshot after checkbox error as checkbox_error.png")
                raise inner_e  # Reraise the exception

        # Step 4: Click the login button
        try:
            # Locate the login button using the provided absolute XPath
            login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
            # Log the button's properties for confirmation
            logging.info(f"Login button text: '{login_button.text}'")
            logging.info(f"Login button class: {login_button.get_attribute('class')}")
            # Scroll to the login button to ensure it's in view
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)  # Wait for scroll to complete
            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", login_button)
            logging.info("Clicked login button.")
        except Exception as e:
            logging.error(f"Unable to click login button: {e}")
            driver.save_screenshot("login_button_error.png")
            logging.info("Saved screenshot after login button error as login_button_error.png")
            raise e

        # Wait for the page reaction after clicking the login button
        time.sleep(5)  # Adjust the wait time based on the actual situation
        logging.info("Waited 5 seconds after clicking the login button.")

        # Take a screenshot after clicking the login button
        driver.save_screenshot("after_login_click.png")
        logging.info("Saved screenshot after login button click as after_login_click.png")

        # Step 5: Click the "China Unicom" button in the pop-up menu
        try:
            # Locate the "China Unicom" button using the provided absolute XPath
            chinese_unicom_button = driver.find_element(By.XPATH, CHINESE_UNICOM_BUTTON_XPATH)
            # Log the button's properties for confirmation
            logging.info(f"China Unicom button text: '{chinese_unicom_button.text}'")
            logging.info(f"China Unicom button class: {chinese_unicom_button.get_attribute('class')}")
            # Scroll to the "China Unicom" button to ensure it's in view
            driver.execute_script("arguments[0].scrollIntoView(true);", chinese_unicom_button)
            time.sleep(1)  # Wait for scroll to complete
            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", chinese_unicom_button)
            logging.info("Clicked 'China Unicom' button.")
        except Exception as e:
            logging.error(f"Unable to click 'China Unicom' button: {e}")
            # Take a screenshot for debugging
            driver.save_screenshot("chinese_unicom_error.png")
            logging.info("Saved screenshot after 'China Unicom' button error as chinese_unicom_error.png")
            raise e  # Reraise the exception

        # Wait for the operation to complete
        time.sleep(3)
        logging.info("Waited 3 seconds after clicking 'China Unicom' button.")

        # Take a screenshot after the operation
        driver.save_screenshot("after_chinese_unicom_click.png")
        logging.info("Saved screenshot after clicking 'China Unicom' button as after_chinese_unicom_click.png")

        # Verify if the login was successful
        try:
            # Assume that a successful login will display an element containing "认证成功"
            success_element = driver.find_element(By.XPATH, AUTH_SUCCESS_XPATH)
            logging.info("Login successful!")
            return True
        except:
            logging.info("Login may not have been successful, please check the script or verify manually.")
            # Take a screenshot for debugging
            driver.save_screenshot("login_failed.png")
            logging.info("Saved screenshot after login failed as login_failed.png")
            return False
    except:
        return False

def auto_login():
    # Configure Firefox browser options
    options = Options()
    options.headless = False  # No need to enable headless mode when using xvfb-run

    # Start Firefox browser
    service = FirefoxService(executable_path='/usr/bin/geckodriver')  # Make sure the geckodriver path is correct
    driver = webdriver.Firefox(service=service, options=options)

    # Set implicit wait (e.g., 10 seconds)
    driver.implicitly_wait(10)

    try:
        logging.info("Automatic login script started.")

        # Open the login page
        driver.get(LOGIN_URL)
        logging.info(f"Opened login page: {LOGIN_URL}")

        # Wait for the page to load
        time.sleep(5)  # Adjust the wait time based on the actual situation
        logging.info("Page loaded.")

        # Check if re-login is required
        if check_auth_success(driver):
            # Perform logout
            perform_logout(driver)
            # Wait for logout to complete
            time.sleep(2)
            logging.info("Logout complete.")

        # Optionally call function to list all buttons
        # buttons = list_buttons(driver)

        # Perform login
        login_success = perform_login(driver, USERNAME, PASSWORD)

        if login_success:
            logging.info("Login process complete.")
        else:
            logging.info("Login process did not complete successfully.")

    except Exception as e:
        logging.error(f"Error during login process: {e}")
        traceback.print_exc()
        # Take a screenshot for debugging
        driver.save_screenshot("error.png")
        logging.info("Saved screenshot after error as error.png")
    finally:
        # Delay to view the result, then close the browser
        time.sleep(5)
        driver.quit()
        logging.info("Firefox browser closed.")

if __name__ == "__main__":
    auto_login()
