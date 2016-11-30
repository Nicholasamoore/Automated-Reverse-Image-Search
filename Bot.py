from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest

class LoginTest(unittest.TestCase):

    # Set up for tineye.com
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.tineye.com")

    # Selects the img-url field and submit button
    def test_Login(self):
        driver = self.driver
        testImageURL      = "http://images.mentalfloss.com/sites/default/files/styles/insert_main_wide_image/public/einstein1_7.jpg"
        urlFieldID        = "url_box"
        submitXpath       = '//*[@id="url_submit"]'
        searchedOverXPath = '/html/body/div[3]/div/div/div[2]/h3[2]/text()[1]'

        urlFieldElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_id(urlFieldID))
        submitElement   = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(submitXpath))

        # Clear the URL field
        urlFieldID.clear()
        # Enter the image URL into the text field
        urlFieldID.send_keys(testImageURL)
        # Click the submit button
        submitElement.click()
        # Wait until the text "Searched Over" is found on results page
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(searchedOverXPath))
        
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
    
##Errors that I am encountering:
##EException ignored in: <bound method Service.__del__ of <selenium.webdriver.firefox.service.Service object at 0x03953710>>
##Traceback (most recent call last):
##  File "C:\Python34\lib\site-packages\selenium\webdriver\common\service.py", line 173, in __del__
##    self.stop()
##  File "C:\Python34\lib\site-packages\selenium\webdriver\common\service.py", line 145, in stop
##    if self.process is None:
##AttributeError: 'Service' object has no attribute 'process'
##
##======================================================================
##ERROR: test_Login (__main__.LoginTest)
##----------------------------------------------------------------------
##Traceback (most recent call last):
##  File "C:\Python34\lib\site-packages\selenium\webdriver\common\service.py", line 74, in start
##    stdout=self.log_file, stderr=self.log_file)
##  File "C:\Python34\lib\subprocess.py", line 859, in __init__
##    restore_signals, start_new_session)
##  File "C:\Python34\lib\subprocess.py", line 1114, in _execute_child
##    startupinfo)
##FileNotFoundError: [WinError 2] The system cannot find the file specified
##
##During handling of the above exception, another exception occurred:
##
##Traceback (most recent call last):
##  File "C:\Users\Nick\Desktop\Programming 1 - Python\Selenium\Bot.py", line 9, in setUp
##    self.driver = webdriver.Firefox()
##  File "C:\Python34\lib\site-packages\selenium\webdriver\firefox\webdriver.py", line 140, in __init__
##    self.service.start()
##  File "C:\Python34\lib\site-packages\selenium\webdriver\common\service.py", line 81, in start
##    os.path.basename(self.path), self.start_error_message)
##selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH. 
##
##
##----------------------------------------------------------------------
##Ran 1 test in 0.056s
##
##FAILED (errors=1)

