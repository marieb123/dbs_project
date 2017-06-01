import csv
from time import strptime

with open('data.csv') as f:
    reader = list(csv.reader(f, delimiter=";"))

cleaned = []
adjusted = 0


for row in reader[1:]:
    #check if handle, text, is_retweet, time, is_quote_status, retweet_count, favourite_count are null
    if not (row[0] and row[1] and row[2] and row[4] and row[6] and row[7] and row[8]):
        continue

    #check if is_retweet==true but no original author or vice versa
    if row[2] == "True" and not row[3] or row[2] == "False" and row[3]:
        continue

    #check if all dates have the same format
    try:
        strptime(row[4], "%Y-%m-%dT%H:%M:%S")
    except:
        continue

    if '\n' in row[1] or '""' in row[1]:
        adjusted +=1

    #replace paragraph with space and ""
    row[1] = row[1].replace("\n"," ")
    row[1] = row[1].replace('""',"")



    # handle, text, is_retweet, original_author, time, is_quote_status, retweet_count, favorite_count
    cleaned.append([row[0], row[1], row[2], row[3], row[4], row[6], row[7], row[8]])

with open('cleaned_data.csv', "w", newline='') as f:
    writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerows(cleaned)

print('adjusted: '+str(adjusted))
print ('deleted: '+str(len(reader)-len(cleaned)-1))
