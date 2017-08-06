"""
"   This script join all 'apis.json', these files need to have the suffix: '[start_index-end_index]', where
"   'start_index' is the index where the crawling starts and 'end_index' is the index where the crawling ends.
"   Dates in Web Service APIs, comments and articles are normalized using timestamp format.
"   This script needs a input parameter which is the number of files you have.
"
"   Example:
"       You have the json files:
"           apis[0-500].json
"           apis[500-1000].json
"           apis[1000-1500].json
"
"       You should execute:
"           $ python cpw_join_apis.py 3
"
"   This script also join users.json files, using the same format.
"
"   @author = "Jael Zela"
"   @contact = "jael.zela@lirmm.fr"
"""

import sys
import json
from datetime import date

##  python -m json.tool output_apis_c.json > output_apis_f.json

if len(sys.argv) < 2:
    print "Introduce the number of files!"
    exit(0)

num_files = int(sys.argv[1])

entries_dict = dict()
empty_entries_dict = dict()

"""
with open("apis_processed.json") as processed_file:
    entries = json.load(processed_file)
    processed_file.close()

    for entry in entries:
        if len(entry['id']) <= 0:
            empty_entries_dict[entry['name']] = entry
        else:
            if entry['name'] in empty_entries_dict:
                del empty_entries_dict[entry['name']]
            entries_dict[entry['id']] = entry
print "Pre-processed:", len(entries_dict.values())
print ""
"""

for i in range(num_files):
    index = i*500
    suffix = "["+str(index)+"-"+str(index+500)+"]"
    file_name = "apis"+suffix+".json"
    print file_name

    with open("data/"+file_name) as data_file:
        entries = json.load(data_file)
        data_file.close()

        for entry in entries:
            if len(entry['id']) <= 0:
                empty_entries_dict[entry['name']] = entry
            else:
                if entry['name'] in empty_entries_dict:
                    del empty_entries_dict[entry['name']]
                for comment in entry['comments']:
                    #print "\tc", str(comment['date'])
                    if "ago" not in str(comment['date']):
                        date_list = str(comment['date']).split()
                        year = -1
                        month = -1
                        day = -1
                        if date_list[2] == "Jan.":
                            month = 1
                        elif date_list[2] == "Feb.":
                            month = 2
                        elif date_list[2] == "Mar.":
                            month = 3
                        elif date_list[2] == "Apr.":
                            month = 4
                        elif date_list[2] == "May.":
                            month = 5
                        elif date_list[2] == "Jun.":
                            month = 6
                        elif date_list[2] == "Jul.":
                            month = 7
                        elif date_list[2] == "Aug.":
                            month = 8
                        elif date_list[2] == "Sep.":
                            month = 9
                        elif date_list[2] == "Oct.":
                            month = 10
                        elif date_list[2] == "Nov.":
                            month = 11
                        elif date_list[2] == "Dec.":
                            month = 12
                        day = int(date_list[3])
                        year = int(date_list[4])
                        comment['date'] = int(date(year, month, day).strftime("%s")) * 1000
                    else:
                        comment['date'] = int(date.today().strftime("%s")) * 1000

                for article in entry['articles']:
                    #print "\ta", str(article['date'])
                    if "ago" not in str(article['date']):
                        date_list = str(article['date']).split("-")
                        year = int(date_list[2])
                        month = int(date_list[0])
                        day = int(date_list[1])
                        article['date'] = int(date(year, month, day).strftime("%s")) * 1000
                    else:
                        article['date'] = int(date.today().strftime("%s")) * 1000

                #print "\tu", str(entry['last_updated'])
                date_list = str(entry['last_updated']).split(".")
                year = int(date_list[2])
                month = int(date_list[0])
                day = int(date_list[1])
                entry['last_updated'] = int(date(year, month, day).strftime("%s")) * 1000

                entries_dict[entry['id']] = entry


output_file = open("dataset_apis_all.json", "w")
output_file.write(json.dumps(entries_dict.values()))
output_file.close()

e_output_file = open("dataset_apis_empty.json", "w")
e_output_file.write(json.dumps(empty_entries_dict.values()))
e_output_file.close()

print "-----------------"

users_dict = dict()

for i in range(num_files):
    index = i*500
    suffix = "["+str(index)+"-"+str(index+500)+"]"
    file_name = "users"+suffix+".json"
    print file_name

    with open("data/"+file_name) as users_file:
        users = json.load(users_file)
        users_file.close()

        for user in users:
            if user['username'] not in users_dict:
                mashups_dict = dict()
                for mashup in user['mashups']:
                    mashups_dict[mashup] = mashup
                user['mashups'] = mashups_dict.keys()

                apis_dict = dict()
                for api in user['apis']:
                    apis_dict[api] = api
                user['apis'] = apis_dict.keys()

                users_dict[user['username']] = user
            else:
                if len(users_dict[user['username']]['name']) == 0 and len(user['name']) > 0:
                    users_dict[user['username']]['name'] = user['name']

                mashups_dict = dict()
                for mashup in users_dict[user['username']]['mashups']:
                    mashups_dict[mashup] = mashup
                for mashup in user['mashups']:
                    mashups_dict[mashup] = mashup
                users_dict[user['username']]['mashups'] = mashups_dict.keys()

                apis_dict = dict()
                for api in users_dict[user['username']]['apis']:
                    apis_dict[api] = api
                for api in user['apis']:
                    apis_dict[api] = api
                users_dict[user['username']]['apis'] = apis_dict.keys()

output_users_file = open("dataset_users.json", "w")
output_users_file.write(json.dumps(users_dict.values()))
output_users_file.close()
print ""
print "Completed APIs:", len(entries_dict.values())
print "APIs to complete:", len(empty_entries_dict.values())
print "Users:", len(users_dict.values())