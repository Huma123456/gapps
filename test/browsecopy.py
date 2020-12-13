from gpapi.googleplay import GooglePlayAPI, RequestError

import pymysql
import sys
import os
import pymysql
import urllib.request
from num2words import num2words
import json

#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="gapps" )
cursor = connection.cursor()

#login
server = GooglePlayAPI("en_US", "UTC")
server.login(None,None,4372181884517069262,'4Qez-s1eEJI4Myt1P_nw20zOpwj7209IFUWyVB76-Pyjb2ZIla5RGnatalrXTVDqi1IZ1A.')

#browse all categories
#***********************shows a list of apps cat>subcat>apps***********************
# apps
print("\nBrowse play store APP categories\n")
categ = "ART_AND_DESIGN"
browse = server.list(cat=categ)
# print(browse)
prevappid=list()#to store ids of previous apps that lie under a category

# for c in browse:
    # print(c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"])
    # categ=c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]#get the name of category
# subcateg=server.list(browse)#get the names of all subcategories of related category
# print(subcateg)


for i in browse:#get the list of all apps of a subcategory
    app=server.list(categ,i,2,1)
    for j in app:
        # print(categ," ",i," ",j['docid'])
            
        #not present before in db then add
        if j['docid'] not in prevappid:   
            insert1 = "INSERT INTO main(aid,cat,subcat) VALUES(%s, %s, %s)"
            val=(j['docid'],"APP",categ)
            cursor.execute(insert1,val)
            prevappid.append(j['docid'])
            
                #fetching the app details 
                # print(j.get('docid'),"\n",j.get('backendDocid'),"\n",j.get('title'),"\n",j.get('creator'),"\n",
                # j.get('descriptionHtml'),"\n",
                # j.get('details').get("appDetails").get("developerName"),"\n",j.get('details').get("appDetails").get("versionString"),"\n",
                # j.get('details').get("appDetails").get("installationSize"),"\n",j.get('details').get("appDetails").get("developerEmail"),"\n",
                # j.get('details').get("appDetails").get("developerWebsite"),"\n",j.get('details').get("appDetails").get("numDownloads"),"\n",
                # j.get('details').get("appDetails").get("packageName"),"\n",j.get('details').get("appDetails").get("recentChangesHtml"),"\n",
                # j.get('details').get("appDetails").get("uploadDate"),"\n",j.get('descriptionShort'))
                
                #get all images of one app and store it in array
                #store comma separated urls in single column for images
            cnt=1
            img=list()
            imgcnvt=list()
            for x in j['image']:
                #converts the number of image into words 
                inttoword=num2words(cnt)
                # Directory 
                directory = j['docid']
                # Parent Directory path 
                # parent_dir = '/mnt/c/xampp/htdocs/appimages/'
                parent_dir='C:/xampp/htdocs/appimages/'
                # Path 
                path = os.path.join(parent_dir, directory) 
                # Create the directory if not exists
                if os.path.isdir(path)==False:   
                    os.mkdir(path) 
                #adds the extension
                exten = path + "/" + inttoword + '.png'
                #downloads it using the two things names and links for each image
                try:
                    urllib.request.urlretrieve(x['imageUrl'],exten)
                except Exception as e:
                    print("exception:: ",e)    
                cnt=cnt+1
                img.append(x['imageUrl'])
                imgcnvt.append(exten)

            #converts both array to json for storing to db
            im = json.dumps(img)
            imcnvt = json.dumps(imgcnvt)
            # s = json.dumps(l1)
            # l2 = json.loads(s)

            insert1 = "INSERT INTO app_details(aid,backendDocid,title,creator,description,img_url,imgurl_convert,devName,version,install_size,dev_email,dev_web,num_downloads,pkg_name,htmlchng,upload_date,desc_short,comment_count) VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s)"
            val=(j.get('docid'),j.get('backendDocid'),j.get('title'),j.get('creator'),j.get('descriptionHtml'),
            im,imcnvt,j.get('details').get("appDetails").get("developerName"),
            j.get('details').get("appDetails").get("versionString"),j.get('details').get("appDetails").get("installationSize"),
            j.get('details').get("appDetails").get("developerEmail"),j.get('details').get("appDetails").get("developerWebsite"),
            j.get('details').get("appDetails").get("numDownloads"),j.get('details').get("appDetails").get("packageName"),
            j.get('details').get("appDetails").get("recentChangesHtml"),j.get('details').get("appDetails").get("uploadDate"),
            j.get('descriptionShort'),j.get('aggregateRating').get('commentCount'))
            cursor.execute(insert1,val)

            insert1 = "INSERT INTO rating(aid,rate_type,star_rate,rate_cnt,one_star,two_star,three_star,four_star,five_star) VALUES(%s,%s, %s, %s,%s, %s, %s,%s, %s)"
            val=(j.get('docid'),j.get('aggregateRating').get('type'),j.get('aggregateRating').get('starRating'),
            j.get('aggregateRating').get('ratingsCount'),j.get('aggregateRating').get('oneStarRatings'),
            j.get('aggregateRating').get('twoStarRatings'),j.get('aggregateRating').get('threeStarRatings'),
            j.get('aggregateRating').get('fourStarRatings'),j.get('aggregateRating').get('fiveStarRatings'))
            cursor.execute(insert1,val)

            # insert1 = "UPDATE main SET status=%s WHERE aid=%s, (aid))"
            cursor.execute("UPDATE main SET status=%s WHERE aid='%s' " % ('1', j.get('docid')))

'''
#games
print("\nBrowse play store GAMES categories\n")
browse=server.browse(cat="GAME")
prevappid=None

for c in browse.get("category"):
    # print(c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"])
    categ=c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]#get the name of category
    subcateg=server.list(categ)#get the names of all subcategories of related category
    # print(subcateg)
    
    for i in subcateg:#get the list of all apps of a subcategory
        app=server.list(categ,i)
        for j in app:
            # print(j['docid']," ",categ," ",i)
            if j['docid']!=prevappid:
                insert1 = "INSERT INTO main(aid,cat,subcat) VALUES(%s, %s, %s)"
                val=(j['docid'],categ,i)
                cursor.execute(insert1,val)
                prevappid=j['docid']
            
'''
connection.commit()
connection.close()