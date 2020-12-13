from gpapi.googleplay import GooglePlayAPI, RequestError

import sys
import os
import pymysql
import urllib.request
from num2words import num2words

#database connection
# connection = pymysql.connect(host="localhost",user="root",passwd="",database="gapps" )
# cursor = connection.cursor()
# gsfId = int(os.environ["GPAPI_GSFID"])
# authSubToken = os.environ["GPAPI_TOKEN"]

server = GooglePlayAPI("en_US", "UTC")

server.login(None,None,4372181884517069262,'4Qez-s1eEJI4Myt1P_nw20zOpwj7209IFUWyVB76-Pyjb2ZIla5RGnatalrXTVDqi1IZ1A.')

'''
gsfId=server.gsfId
AuthToken = server.authSubToken
# print(gsfId, "\n", AuthToken)

# LOGIN
print("\nLogin with ac2dm token and gsfId saved\n")

# SEARCH
print("\nSearch suggestion for \"fir\"\n")
print(server.searchSuggest("fir"))

result = server.search("firefox")
i=0
for doc in result:
    if 'docid' in doc:
        print("doc: {}".format(doc["docid"]))
    for cluster in doc["child"]:
        # print(cluster)
        print("\tcluster: {}".format(cluster["docid"]))
        for app in cluster["child"]:
            # print(app)
            print("\t\tapp: {}".format(app["docid"]))
            # c=cluster['docid']
            # a=app['docid']
            # print(c, "\n", a)
            insert1 = "INSERT INTO Artists(NAME, TRACK) VALUES(%s, %s)"
            val=(cluster['docid'],app['docid'])
            cursor.execute(insert1,val)
connection.commit()
connection.close()

# HOME APPS
print("\nFetching apps from play store home\n")
result = server.home()
for doc in result:
    print('first')
    if 'docid' in doc:
        print('found')
        print("doc: {}".format(doc["docid"]))
    for cluster in doc["child"]:
        print('foundcluster')
        print("\tcluster: {}".format(cluster["docid"]))
        for app in cluster["child"]:
            print('foundapp')
            print("\t\tapp: {}".format(app["docid"]))

# DOWNLOAD
docid = "org.mozilla.focus"
server.log(docid)
print("\nAttempting to download {}\n".format(docid))
fl = server.download(docid)
with open(docid + ".apk", "wb") as apk_file:
    print('inside')
    for chunk in fl.get("file").get("data"):
        apk_file.write(chunk)
    print("\nDownload successful\n")

# BULK DETAILS
testApps = ["org.mozilla.focus", "com.non.existing.app"]
bulk = server.bulkDetails(testApps)

print("\nTesting behaviour for non-existing apps\n")
if bulk[1] is not None:
    print("bulkDetails should return empty dict for non-existing apps")
    sys.exit(1)

print("\nResult from bulkDetails for {}\n".format(testApps[0]))
print(bulk[0]["docid"])

testApps = ["org.mozilla.rocket", "com.non.existing.app"]

# DETAILS
print("\nGetting details for %s\n" % testApps[0])
details = server.details(testApps[0])
#fetching the details 
print(details['docid'],"\n",details['backendDocid'],"\n",details['title'],"\n",details['creator'],"\n",
details['descriptionHtml'],"\n",
details['details']["appDetails"]["developerName"],"\n",details['details']["appDetails"]["versionString"],"\n",
details['details']["appDetails"]["installationSize"],"\n",details['details']["appDetails"]["developerEmail"],"\n",
details['details']["appDetails"]["developerWebsite"],"\n",details['details']["appDetails"]["numDownloads"],"\n",
details['details']["appDetails"]["packageName"],"\n",details['details']["appDetails"]["recentChangesHtml"],"\n",
details['details']["appDetails"]["uploadDate"],"\n",details['descriptionShort'])
x="one"
# insert1 = "INSERT INTO Artists(aid,backendDocid,titlecreator,description,img_url,devName,version,install_size,dev_email,dev_web,num_downloads,pkg_name,htmlchng,upload_date,desc_short) VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
# val=(,"two","th","one","two","th","one","two","th","one","two","th","one","two","th","on")


#store comma separated urls in single column for images
print("ImageUrl")
cnt=1
img=list()
imgcnvt=list()
for x in details['image']:
     #converts the number of image into words 
    inttoword=num2words(cnt)
    # Directory 
    directory = details['docid']
    # Parent Directory path 
    parent_dir = '/mnt/c/xampp/htdocs/appimages/'
    # Path 
    path = os.path.join(parent_dir, directory) 
    # Create the directory if not exists
    if os.path.isfile(path)==True:   
        os.mkdir(path) 
    #adds the extension
    exten = path + "/" + inttoword + '.png'
    #downloads it using the two things names and links for each image
    urllib.request.urlretrieve(x['imageUrl'],exten)
    cnt=cnt+1
    img.append(x['imageUrl'])
    imgcnvt.append(exten)
print(img, imgcnvt)


#make separate table for rating
print("Aggregate rating")
for y in details['aggregateRating'].values():
    print(y)

print("file description")
for y in details['details']["appDetails"]["file"]:
    print("VersionCode",y["versionCode"])
    print("Size",y["size"])

testApps = ["org.mozilla.focus", "com.non.existing.app"]
# REVIEWS
print("\nGetting reviews for %s\n" % testApps[0])
revs = server.reviews(testApps[0])
print(revs)
for r in revs:
    print(
        r["userProfile"]["personIdString"],
        str(r["starRating"]))
    for x in r["userProfile"]["image"]:
        print('imgURL',x['imageUrl'])


# BROWSE
print("\nBrowse play store categories\n")
browse = server.browse()
for c in browse.get("category"):
    print(c["name"])


#getting the nested value
sampleCat = browse["category"][0]["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
print("\nBrowsing the {} category\n".format(sampleCat))
browseCat = server.home(cat=sampleCat)

for doc in browseCat:
    if 'docid' in doc:
        print("doc: {}".format(doc["docid"]))
    for child in doc["child"]:
        print("\tsubcat: {}".format(child["docid"]))
        for app in child["child"]:
            print(app)
            print("\t\tapp: {}".format(app["docid"]))


#***********************shows a list of apps cat>subcat>apps***********************
# apps
print("\nBrowse play store APP categories\n")
browse = server.browse()
prevappid=list()#to store ids of previous apps that lie under a category

for c in browse.get("category"):
    # print(c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"])
    categ=c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]#get the name of category
    subcateg=server.list(categ)#get the names of all subcategories of related category
    # print(subcateg)
    
    for i in subcateg:#get the list of all apps of a subcategory
        app=server.list(categ,i)
        for j in app:
            # print(categ," ",i," ",j['docid'])
            if j['docid'] not in prevappid:
                # print('not present')   
                insert1 = "INSERT INTO main(aid,cat,subcat) VALUES(%s, %s, %s)"
                val=(j['docid'],categ,i)
                cursor.execute(insert1,val)
                prevappid.append(j['docid'])
    print(prevappid)
            
# #games
# print("\nBrowse play store GAMES categories\n")
# browse=server.browse(cat="GAME")
# for c in browse.get("category"):
#     # print(c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"])
#     categ=c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]#get the name of category
#     subcateg=server.list(categ)#get the names of all subcategories of related category
#     # print(subcateg)
    
#     for i in subcateg:#get the list of all apps of a subcategory
#         app=server.list(categ,i)
#         prevappid=None
#         for j in app:
#             # print(j['docid']," ",categ," ",i)
#             if j['docid']!=prevappid:
#                 insert1 = "INSERT INTO main(aid,cat,subcat) VALUES(%s, %s, %s)"
#                 val=(j['docid'],categ,i)
#                 cursor.execute(insert1,val)
#             prevappid=j['docid']
            
connection.commit()
connection.close()

# print(server.list("TRAVEL_AND_LOCAL", ctr="apps_topselling_free"))

#to get the game categories
#print(server.browse(cat="GAME"))

# LIST
# cat = "MUSIC_AND_AUDIO"
# print("\nList {} subcategories\n".format(cat))
# server.alllist(cat)


for c in catList:
    print(c)

limit = 4
print("\nList only {} apps from subcat {} for {} category\n".format(
    limit, catList[0], cat))
appList = server.list(cat, catList[0], 4, 1)
for app in appList:
    print(app["docid"])
'''