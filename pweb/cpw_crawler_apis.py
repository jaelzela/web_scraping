"""
"   This script crawl each Web Service API from a list, json APIs file (crawled by cpw_crawler_apis_browse.py),
"   the input file for this script should be named 'apis_to_process.json'.
"   Description, mashups, articles, comments, developers, followers are collected for each Web Service API;
"   at the same time Users are collected from developers and followers sections.
"   A backup is saved each 20 crawled APIs ('apis_all.json', 'users_all.json').
"   At the end, analytic information is calculated and displayed.
"
"   NOTE: this script receive a parameter which is the start index of the APIs list and crawl the 500 APIs starting
"   from the start index. This was implemented in this way to get multiple scripts running at the same time.
"   To run multiples times this script, you need to have different copies of this in diferente folders.
"
"   @author = "Jael Zela"
"   @contact = "jael.zela@lirmm.fr"
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import json
import operator
import sys

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
        self.articles = []


### Comment entity for a Web Service API
class Comment:
    user = ""
    date = ""
    comment = ""

    def __init__(self):
        self.user = ""
        self.date = ""
        self.comment = ""


### Article entity for a Web Service API
class Article:
    user = ""
    date = ""
    title = ""
    type = ""
    categories = []
    resume = ""

    def __init__(self):
        self.user = ""
        self.date = ""
        self.title = ""
        self.type = ""
        self.categories = []
        self.resume = ""


### User entity for a Web Service API
class User:
    username = ""
    name = ""
    mashups = []
    apis = []

    def __init__(self):
        self.username = ""
        self.name = ""
        self.mashups = []
        self.apis = []


### Function to calculate the maximum and minimum value from a list of integers
def calculate_analytics(counter_list):
    sum_value = 0
    x, max_value = max(enumerate(counter_list), key=operator.itemgetter(1))
    y, min_value = min(enumerate(counter_list), key=operator.itemgetter(1))
    for count in counter_list:
        sum_value += count
    return sum_value, max_value, min_value


### Input Parameters to define the start point to crawl
if len(sys.argv) < 2:
    print "Introduce the start point index!"
    exit(0)

start_index = int(sys.argv[1])
print start_index, (start_index + 500)

### General Variables
comments_count_list = []
followers_count_list = []
developers_count_list = []
articles_count_list = []
mashups_count_list = []
users = dict()

### Load previous users.
with open('data/users_all.json') as data_file:
    users_json = json.load(data_file)
    for user in users_json:
        users[user['username']] = user
    data_file.close()

### Open WebDriver Selenium
URL_domain = "http://www.programmableweb.com"
driver = webdriver.Firefox()
driver.implicitly_wait(5)
driver.maximize_window()

### Load Web Service APIs to process
with open('data/apis_to_process.json') as data_file:
    entries = json.load(data_file)
    data_file.close()

    counter = 1
    for entry in entries[start_index: (start_index + 500)]:

        if len(entry['id']) > 0:
            counter += 1
            continue

        # Load Web Service API
        driver.get(entry['reference'])

        # DESCRIPTION
        try: description = driver.find_element_by_xpath("//div[@class='api_description tabs-header_description']").text
        except NoSuchElementException, e: description = ""

        # Look for myTabContent (the content container).
        try: content = driver.find_element_by_xpath("//div[@id='myTabContent']")
        except NoSuchElementException, e:
            print entry
            counter += 1
            continue
        elements = content.find_elements_by_xpath(".//div[@class='block-title']")

        # ID
        entry_article = driver.find_element_by_xpath("//section[@id='block-system-main']/article")
        id_entry = entry_article.get_attribute("id").split("-")[1]

        # MASHUPS
        mashups_title = elements[3].find_element_by_xpath(".//span").text
        mashups = int(mashups_title[mashups_title.index("(")+1:mashups_title.index(")")])

        # ARTICLES
        articles = []
        if len(elements) > 4 and elements[4].find_element_by_xpath(".//span").text == "RELATED ARTICLES":
            driver.get(URL_domain+"/category/all/news?apis="+id_entry)

            while True:
                articles_list = driver.find_elements_by_xpath("//section[@id='block-system-main']/article/div/div[@class='view-content']/div[contains(@class, 'views-row')]")

                for article in articles_list:
                    article_title = article.find_element_by_xpath(".//h2/a").text
                    article_resume = article.find_element_by_xpath(".//div[@class='text']/span").text
                    article_type = article.find_element_by_xpath(".//div[@class='pull-left-wrapper']/div[@class='pull-left tags content-type']").text
                    article_user = article.find_element_by_xpath(".//div[@class='pull-left-wrapper']/div[@class='pull-left name']").text
                    try: article_categories = article.find_element_by_xpath(".//div[@class='pull-left-wrapper']/div[@class='pull-left tags']").text.split(", ")
                    except NoSuchElementException, e: article_categories = []
                    article_date = article.find_element_by_xpath(".//div[@class='pull-left-wrapper']/div[@class='pull-left date']").text

                    art = Article()
                    art.title = article_title
                    art.resume = article_resume
                    art.type = article_type
                    art.user = article_user
                    art.categories = article_categories
                    art.date = article_date

                    articles.append(art.__dict__)

                try: next_page = driver.find_element_by_xpath("//ul[@class='pagination']/li[@class='pager-last last']/a")
                except NoSuchElementException, e: break
                next_page.click()

        # FOLLOWERS
        driver.get(entry['reference']+"/followers")
        content = driver.find_element_by_xpath("//div[@id='myTabContent']")

        while True:
            try:
                time.sleep(2)
                load_more = content.find_element_by_id("pager_id_list_all")
                load_more.click()
                time.sleep(3)
            except NoSuchElementException, e: break

        followers_list = content.find_elements_by_xpath(".//div[@id='followers']/div/div/table/tbody/tr/td[@class='views-field views-field-name']")
        followers = []
        for element in followers_list:
            followers.append(element.text)
            if element.text not in users:
                user = dict()
                user['username'] = element.text
                user['name'] = ""
                user['mashups'] = []
                user['apis'] = []
                users[element.text] = user

            users[element.text]['apis'].append(entry['name'])

        # DEVELOPERS
        driver.get(entry['reference']+"/developers")
        content = driver.find_element_by_xpath("//div[@id='myTabContent']")

        while True:
            try:
                time.sleep(2)
                load_more = content.find_element_by_id("pager_id_list_all")
                load_more.click()
                time.sleep(3)
            except NoSuchElementException, e: break

        developers_list = content.find_elements_by_xpath(".//div[@id='developers']/div/div/table/tbody/tr")
        developers = dict()
        for element in developers_list:
            username = element.find_element_by_class_name("views-field-name").text
            name = element.find_element_by_class_name("views-field-nothing").text
            mashup = element.find_element_by_class_name("views-field-title").text
            #username = element.find_element_by_xpath(".//td[@class='views-field views-field-name']").text
            #name = element.find_element_by_xpath(".//td[@class='views-field views-field-nothing']").text
            #mashup = element.find_element_by_xpath(".//td[@class='views-field views-field-title']").text

            developers[username] = username
            if element.text not in users:
                user = dict()
                user['username'] = username
                user['name'] = ""
                user['mashups'] = []
                user['apis'] = []
                users[username] = user

            users[username]['name'] = name
            users[username]['mashups'].append(mashup)

        # COMMENTS
        driver.get(entry['reference'] + "/comments")
        content = driver.find_element_by_xpath("//div[@id='myTabContent']")

        try: comments_list = content.find_elements_by_xpath(".//div[@id='comments']/article")
        except NoSuchElementException, e: comments_list = []

        comments = []
        for cmnt in comments_list:
            try:
                comment_user = cmnt.find_element_by_xpath(".//div[@class='author-datetime']/a").text
            except NoSuchElementException, e:
                comment_user = cmnt.find_element_by_xpath(".//div[@class='author-datetime']/span").text
            comment_date = cmnt.find_element_by_xpath(".//div[@class='author-datetime']").text
            comment_date = comment_date[len(comment_user):]
            div = cmnt.find_element_by_xpath(".//div[@class='comment-text']")
            comment_text = div.find_element_by_xpath(".//p").text

            comment = Comment()
            comment.user = comment_user.strip()
            comment.date = comment_date.strip()
            comment.comment = comment_text.strip()

            comments.append(comment.__dict__)

        # Set values to the entry
        entry['id'] = id_entry
        entry['description'] = description.encode('utf-8')
        entry['followers'] = followers
        entry['developers'] = developers.keys()
        entry['mashups'] = mashups
        entry['articles'] = articles
        entry['comments'] = comments

        # Counters (Analytics)
        followers_count_list.append(len(followers))
        developers_count_list.append(len(developers.keys()))
        mashups_count_list.append(mashups)
        comments_count_list.append(len(comments))
        articles_count_list.append(len(articles))

        # Save a backup each 20 APIs
        if counter % 20 == 0:
            file_api = open('data/apis_all.json', 'w')
            file_api.write(json.dumps(entries))
            file_api.close()

            file_user = open('data/users_all.json', 'w')
            file_user.write(json.dumps(users.values()))
            file_user.close()

        counter += 1
    # Close WebDriver Selenium
    driver.quit()

    # Write in a json file
    file_apis = open('data/apis.json', 'w')
    file_apis.write(json.dumps(entries))
    file_apis.close()

    # Print analytics information
    print "Entries:", len(entries)
    print "Entries this time:", counter
    print "\n"
    f_sum, f_max, f_min = calculate_analytics(followers_count_list)
    print "Followers:", f_sum
    print "Max Followers:", f_max
    print "Min Followers:", f_min
    print "\n"
    d_sum, d_max, d_min = calculate_analytics(developers_count_list)
    print "Developers:", d_sum
    print "Max Developers:", d_max
    print "Min Developers:", d_min
    print "\n"
    m_sum, m_max, m_min = calculate_analytics(mashups_count_list)
    print "Mashups:", m_sum
    print "Max Mashups:", m_max
    print "Min Mashups:", m_min
    print "\n"
    c_sum, c_max, c_min = calculate_analytics(comments_count_list)
    print "Comments:", c_sum
    print "Max Comments:", c_max
    print "Min Comments:", c_min
    print "\n"
    a_sum, a_max, a_min = calculate_analytics(articles_count_list)
    print "Articles:", a_sum
    print "Max Articles:", a_max
    print "Min Articles:", a_min
    print "\n"

    # Write in a json file
    file_users = open('data/users.json', 'w')
    file_users.write(json.dumps(users.values()))
    file_users.close()