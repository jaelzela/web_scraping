"""
"   This script filter Web Service APIs with comments, if a Web Service API has at least one comment,
"   it is saved in another json file.
"
"   @author = "Jael Zela"
"   @contact = "jael.zela@lirmm.fr"
"""
import json

with open('dataset_apis_all.json') as data_file:
    entries = json.load(data_file)
    data_file.close()

    entries_list = []
    for entry in entries:
        if len(entry['comments']) > 0:
            entries_list.append(entry)

output_file = open("dataset_apis.json", "w")
output_file.write(json.dumps(entries_list))
output_file.close()

print "APIs:", len(entries)
print "Commented APIs:", len(entries_list)