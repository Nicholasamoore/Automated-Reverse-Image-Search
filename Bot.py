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

        urlFieldElement  = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_id(urlFieldID))
        submitElement    = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(submitXpath))

        #print(topResultElement)
        # Clear the URL field
        urlFieldElement.clear()
        # Enter the image URL into the text field
        urlFieldElement.send_keys(testImageURL)
        # Click the submit button
        submitElement.click()
        # Wait until the text "Searched Over" is found on results page
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(searchedOverXPath))

        # Retrieve the current URL and navigate to the sort-by-biggest page
        currentURL  = driver.current_url
        driver.get(currentURL + '?sort=size&order=desc')

        # Retrieve the dimensions of the first image shown
        newImageDimenXpath = '//*[@class="row matches"]/div/div[1]/div[2]/p[1]/span[2]'
        newImageDimensions = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(newImageDimenXpath))

        # Store the element's dimensions as a string 
        newDimensions = newImageDimensions.text[:-1]

        # Split string by 'x' and create list, store into horizontal & vertical variables
        dimensionsList = newDimensions.split('x')
        newHorizontal = dimensionsList[0]
        newVertical   = dimensionsList[1]

        # Temporary variables until I figure out how to get the Redditor's image dimensions
        oldHorizontal = 1
        oldVertical   = 2

        if int(newHorizontal)*int(newVertical) > int(oldHorizontal)*int(oldVertical):
            # Retrieve the new image URL
            newImageXpath = '//*[@class="row matches"]/div/div[1]/div[2]/a[1]/img/@src'
            newImageURL   = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(newImageXpath))
            newImageURL   = newImageURL.text
            print(newImageURL) # Testing purposes
        else:
            userMessage = "Sorry, a larger image cannot be found."

        
        
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
