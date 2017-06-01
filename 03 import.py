import psycopg2.extras
import csv
import re

# Try to connect
try:
    conn = psycopg2.connect("dbname='Election' user='postgres' host='localhost' password='123'")
except:
    print ("Cannot Connect!")

# get cursor and proceed query
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

with open('cleaned_data.csv') as f:
    reader = list(csv.reader(f, delimiter=";"))


# insert data into tweet
tweet_id = 0
for row in reader:
    tweet_id += 1
    cur.execute(""" INSERT INTO tweet
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" , (tweet_id,row[0],row[1],row[2],row[3], row[4], row[5], row[6], row[7]))
            # id, handle, text, is_retweet, original_author, time, is_quote_status, retweet_count, favorite_count


#extract hashtags from text and insert them into hashtag_table and contains
hashtag_list=[]
tweet_id=0

for row in reader:
    tweet_id+=1
    #extract hashtags from text
    hashtags_per_tweet = re.findall('#[A-Za-z0-9]+',row[1])

    #insert all unique hashtags into hashtag_table
    for hashtag in hashtags_per_tweet:
        if hashtag not in hashtag_list:
            hashtag_list.append(hashtag)
            cur.execute("""INSERT INTO hashtag_table VALUES ('%s')""" % (hashtag))

        #insert all hashtags and respective tweet_ids into contains
        cur.execute("""INSERT INTO contains VALUES (%s, %s)""" , (tweet_id, hashtag))

conn.commit()

