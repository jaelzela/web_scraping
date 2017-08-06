"""
"   This script extract all comments for each Web Service API, to save all comments in a single json file,
"   for each comment an 'api' element is added with the API ID.
"
"   @author = "Jael Zela"
"   @contact = "jael.zela@lirmm.fr"
"""

import json

with open('dataset_apis.json') as data_file:
    entries = json.load(data_file)
    data_file.close()

    comments_list = []
    for entry in entries:
        for comment in entry['comments']:
            comment['api'] = entry['id']
            comments_list.append(comment)

print "APIs:", len(entries)

output_file = open("dataset_comments.json", "w")
output_file.write(json.dumps(comments_list))
output_file.close()