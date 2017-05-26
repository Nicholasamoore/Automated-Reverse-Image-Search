import praw
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

infile = open('pass.txt', 'r')
password = infile.readline()
infile.close()

r = praw.Reddit(user_agent = "Created by Nicholas Moore")
r.login('HighResolutionBot', password)
print("Logging in...")

def compare_images(newWidth,newHeight,oldWidth,oldHeight,newImageURL):
    # Compare the two image dimensions
    if int(newWidth)*int(newHeight) > int(oldWidth)*int(oldHeight):
        userMessage = "Success! I found a larger image [here](" + newImageURL + ")" + "\n\n" + \
                       "Old image: " + oldWidth + "x" + oldHeight + "\n" + "| " + \
                       "New image: " + newWidth + "x" + newHeight 
    else:
        userMessage = "Sorry! I located your image but could not find a higher resolution."
    return userMessage

def image_search(source_url):
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    driver.get(source_url)

    imagexpath = driver.find_element_by_xpath('//*[@id="5Q93S9L"]/div[1]/img')
    img_src = imagexpath.get_attribute("src")

    driver.get("https://images.google.com/")

    redditImageURL = img_src

    # Find and click the photo icon
    photoIconXpath = '//*[@id="qbi"]'
    photoIcon      = driver.find_element_by_xpath(photoIconXpath)
    photoIcon.click()

    # Find the search field and paste source_url
    searchFieldXpath = '//*[@id="qbui"]'
    searchField = driver.find_element_by_xpath(searchFieldXpath)
    searchField.send_keys(redditImageURL)


    # Find and click "Search by image" button
    searchButtonXpath = '//*[@id="qbbtc"]/input'
    searchButton = driver.find_element_by_xpath(searchButtonXpath)
    searchButton.click()

    try:
        # Find and click "All sizes" text
        largeTextXpath = '//*[@id="_w6"]/div[2]/span[1]/a'
        largeText = driver.find_element_by_xpath(largeTextXpath)
        largeText.click()
        
        # Locate the first image result and open url
        firstImageXpath = '//*[@id="rg_s"]/div[1]/a/img'
        firstImage = driver.find_element_by_xpath(firstImageXpath)
        firstImage.click()

        # Click on "View Image"
        #viewImageXpath = '//*[@id="irc_cc"]/div[2]/div[3]/div[1]/div/div[2]/table[1]/tbody/tr/td[2]/a/span'
        viewImageButton = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_link_text('View image'))
        newImageURL = viewImageButton.get_attribute('href')

        # Get the current image URL
        print(str(newImageURL))
        driver.get(newImageURL)
        
        # Retrieve the dimensions of the new image
        sourceElement1 = driver.find_element_by_xpath('/html/body/img')
        newWidth = sourceElement1.get_attribute('naturalWidth')
        newHeight = sourceElement1.get_attribute('naturalHeight')
        
        # Switch to source image URL on browser
        driver.get(redditImageURL)
        
        # Retrieve the dimensions of the source image
        sourceElement2  = driver.find_element_by_xpath('/html/body/img')
        oldWidth = sourceElement2.get_attribute('naturalWidth')
        oldHeight = sourceElement2.get_attribute('naturalHeight')

        userMessage = compare_images(newWidth,newHeight,oldWidth,oldHeight,newImageURL)
    except NoSuchElementException:
        userMessage = "Sorry, I could not find this image on Google!"

    driver.quit()
    return userMessage
        
def run_bot():
    cache = []
    infile = open('cache.txt','r')
    for line in infile:
        line = line.rstrip('\n')
        cache.append(line)
    infile.close()
    
    keyWord = ['!hiresbot', 'hiresbot']
    
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
            print("Submission URL found!")
            
            # Pass the submission URL to image_search() to compare dimensions
            userMessage = image_search(submissionURL)
            
            comment.reply(userMessage)
            print("Reply successful!")
            
            outfile = open('cache.txt','a')
            outfile.write(comment.id + '\n')
            outfile.close()
            
    print("Comments loop finished, time to sleep")

while True:
    run_bot()
    time.sleep(20)
