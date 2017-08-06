"""
"   This script crawl the Web Services APIs Browser, going through all pages collecting
"   the name, category, url reference and last update date for each Web Service
"
"   @author = "Jael Zela"
"   @contact = "jael.zela@lirmm.fr"
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import json

### Entry entity for a Web Service API
class Entry:
    id = ""
    name = ""
    description = ""
    reference = ""
    category = ""
    last_updated = ""
    comments = []
    followers = []
    developers = []
    mashups = 0
    articles = []

    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""
        self.reference = ""
        self.category = ""
        self.last_updated = ""
        self.comments = []
        self.followers = []
        self.developers = []
        self.mashups = 0
        self.articles = 0

### General Variables
comments_count_list = []
followers_count_list = []
developers_count_list = []
articles_count_list = []
mashups_count_list = []
users_dict = dict()

### Open WebDriver Selenium
URL_domain = "http://www.programmableweb.com"
driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(URL_domain+"/apis/directory?order=created&sort=desc")
driver.maximize_window()

entries = []
### Iterate through the pagination for Web Services APIs
while True:
    elements = driver.find_elements_by_xpath("//div/section/article/div/div[@class='view-content']/table/tbody/tr")
    for element in elements:
        name = element.find_element_by_xpath(".//td[1]/a").text                       # Name
        reference = element.find_element_by_xpath(".//td[1]/a").get_attribute("href") # Reference
        try: category = element.find_element_by_xpath(".//td[3]/a").text              # Category
        except NoSuchElementException, e: category = ""
        last_updated = element.find_element_by_xpath(".//td[4]").text                 # Last Updated

        # Set values to the Entry
        entry = Entry()
        entry.name = name
        entry.reference = reference
        entry.category = category
        entry.last_updated = last_updated

        entries.append(entry)

    # Go to the next page
    try: next_page = driver.find_element_by_xpath("//ul[@class='pagination']/li[@class='pager-last last']/a")
    except NoSuchElementException, e: break     # finish iterations
    next_page.click()
    time.sleep(3)
# Close WebDriver Selenium
driver.quit()

# Convert entries to dictionaries
entries_dicts_list = []
for entry in entries:
    entries_dicts_list.append(entry.__dict__)

# Write in a json file
file = open('data/apis_list.json', 'w')
file.write(json.dumps(entries_dicts_list))
file.close()

# Print analytics information
print "Entries:", len(entries)
print "\n"