import random
import psycopg2.extras
import distance
import csv


def midpoint(cluster):
    if cluster:
        maximum_distance = [(max(dist(hashtag, h) for h in cluster)) for hashtag in cluster]
        minimum_distance = min(maximum_distance)
        index =  maximum_distance.index(minimum_distance)
        return cluster[index]
    else:
        return ''

def dist(x,y):
    return distance.levenshtein(x, y)

# Try to connect
try:
    conn = psycopg2.connect("dbname='Election' user='postgres' host='localhost' password='123'")
except:
    print ("Cannot Connect!")

# get cursor and proceed query
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

try:
    cur.execute("""SELECT * from hashtag_table""")
except:
    print ("Cannot Select!")

hashtags = []
rows = cur.fetchall()
for row in rows:
    hashtags.append(row[0].lower())


# define maximum number of clusters
number_of_clusters = 7
center_new=[]
center=[]
center_dist = [0]*len(center)


# generate centers of clusters at random
for i in range(number_of_clusters):
    word = hashtags[random.randint(0, len(hashtags)-1)]
    if word not in center_new:
        center_new.append(word)
        center.append('a')
print("center: "+str(center_new))

# k-means
while max(dist(center[i],center_new[i]) for i in range(len(center)))>0:

    # flush cluster
    cluster= [[] for i in range(len(center))]
    # copy previous centerpoints
    center= [center_new[i] for i in range(len(center))]

    # assign cluster to hashtags
    for tag in hashtags:
        # find closest centerpoint
        min_center = center[0]
        index = 0
        for i in range(len(center)):
            if dist(tag,center[i])<dist(tag,min_center):
                min_center = center[i]
                index = i
        # assign hashtag to cluster
        cluster[index].append(tag)

    # find new centerpoints for clusters
    for i in range(len(center)):
        center_new[i]=midpoint(cluster[i])

    print("center: "+str(center_new))

for i in range(len(cluster)):
    print("cluster "+str(i)+": "+str(cluster[i]))

# preparation for visualization
cluster = [sorted(c, key=lambda s: len(s)) for c in cluster]

with open('clusters_export_'+str(number_of_clusters)+'.csv', "w", newline='') as f:
    writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerow(['cluster_name','hashtags','size'])
    for i in range(len(cluster)):
        summary = ''
        for j in range(len(cluster[i])):
            summary+=(cluster[i][j]+' ')
        writer.writerow(['Cluster '+str(i),summary,len(cluster[i])])
