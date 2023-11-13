# Made by AI to get a start

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
def fill_panorama_survey(name: str, email: str, age: int, rating: int):
    """
    Function to fill out a Panorama Survey online.
 
    Parameters:
    - name: str
        The name of the person filling out the survey.
    - email: str
        The email address of the person filling out the survey.
    - age: int
        The age of the person filling out the survey.
    - rating: int
        The rating given by the person filling out the survey.
 
    Returns:
    - bool:
        Returns True if the survey was successfully filled out, False otherwise.
    """
 
    # Set up the Chrome driver
    driver_service = Service('path/to/chromedriver')  # Replace with the actual path to your chromedriver executable
    driver = webdriver.Chrome(service=driver_service)
 
    try:
        # Open the Panorama Survey website
        driver.get('https://www.panoramasurvey.com')
 
        # Fill out the name field
        name_field = driver.find_element(By.ID, 'name')
        name_field.send_keys(name)
 
        # Fill out the email field
        email_field = driver.find_element(By.ID, 'email')
        email_field.send_keys(email)
 
        # Fill out the age field
        age_field = driver.find_element(By.ID, 'age')
        age_field.send_keys(str(age))
 
        # Select the rating
        rating_field = driver.find_element(By.ID, 'rating')
        rating_options = rating_field.find_elements(By.TAG_NAME, 'option')
        rating_options[rating - 1].click()
 
        # Submit the survey
        submit_button = driver.find_element(By.ID, 'submit')
        submit_button.click()
 
        # Wait for the success message
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'success-message'))
        )
 
        return True
 
    except Exception as e:
        print(f"Error occurred while filling out the survey: {e}")
        return False
 
    finally:
        # Close the browser
        driver.quit()
 
# Example usage of the fill_panorama_survey function
name = "John Doe"
email = "johndoe@example.com"
age = 25
rating = 4
 
success = fill_panorama_survey(name, email, age, rating)
if success:
    print("Survey successfully filled out.")
else:
    print("Failed to fill out the survey.")