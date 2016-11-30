from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest

class LoginTest(unittest.TestCase):

    # Set up for tineye.com
    def setUp(self):
        self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        self.driver.get("https://www.tineye.com")

    # Selects the img-url field and submit button
    def test_Login(self):
        driver = self.driver
        testImageURL      = "http://images.mentalfloss.com/sites/default/files/styles/insert_main_wide_image/public/einstein1_7.jpg"
        urlFieldID        = "url_box"
        submitXpath       = '//*[@id="url_submit"]'
        searchedOverXPath = '//*[@id="sort_selector"]'

        urlFieldElement = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_id(urlFieldID))
        submitElement   = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(submitXpath))

        # Clear the URL field
        urlFieldElement.clear()
        # Enter the image URL into the text field
        urlFieldElement.send_keys(testImageURL)
        # Click the submit button
        submitElement.click()
        # Wait until the text "Searched Over" is found on results page
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(searchedOverXPath))
        
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
