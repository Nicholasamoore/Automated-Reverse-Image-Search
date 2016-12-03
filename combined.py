import praw
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

r = praw.Reddit(user_agent = "Created by Nicholas Moore")
print("Logging in...")

infile = open('pass.txt', 'r')
password = infile.readline()
infile.close()
r.login('HighResolutionBot', password)

keyWord = ['!hiresbot', 'hiresbot']
cache = []

def image_search(source_url):
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver.get("https://www.tineye.com")

    redditImageURL    = source_url
    urlFieldID        = "url_box"
    submitXpath       = '//*[@id="url_submit"]'
    searchedOverXPath = '//*[@id="sort_selector"]'

    urlFieldElement  = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_id(urlFieldID))
    submitElement    = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(submitXpath))

    # Clear the URL field
    urlFieldElement.clear()
    # Enter the image URL into the text field
    urlFieldElement.send_keys(redditImageURL)
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
    newWidth  = dimensionsList[0]
    newHeight = dimensionsList[1]

    # Retrieve the new image URL
    newImageXpath = '//*[@class="row matches"]/div/div[1]/div[2]/a[1]/img/@src'
    newImageURL   = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_xpath(newImageXpath))
    newImageURL   = newImageURL.text
  
    # Switch to source image URL on browser
    driver.get(redditImageURL)
    
    # Retrieve the dimensions of the source image
    oldWidth  = driver.findElement('/html/body/img').getSize().getWidth()
    oldHeight = driver.findElement('/html/body/img').getSize().getHeight()

    if int(newWidth)*int(newHeight) > int(oldWidth)*int(oldHeight):
        userMessage = "Success! I found a larger image at: " + newImageURL
    else:
        userMessage = "Sorry, I could not find a larger image."
    return userMessage
        
    driver.quit()


def run_bot():
    print("Grabbing subreddit...")
    subreddit = r.get_subreddit("test")

    print("Grabbing comments...")
    comments = subreddit.get_comments(limit = 200)

    for comment in comments:
        comment_text = comment.body.lower()

        isMatch = any(string in comment_text for string in keyWord)

        if comment.id not in cache and isMatch:
            print("Match found! Comment ID: " + comment.id)
            print("Finding submission URL...")

            # Grab the submission's image URL linked to the comment
            submissionURL = comment.submission.url
            
            # Pass the submission URL to image_search() to compare dimensions
            userMessage = image_search(submissionURL)

            comment.reply(userMessage)
            print("Reply successful!")

            cache.append(comment.id)
    print("Comments loop finished, time to sleep")

while True:
    run_bot()
    time.sleep(10)
