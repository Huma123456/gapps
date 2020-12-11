from gpapi.googleplay import GooglePlayAPI, RequestError

import pymysql
import sys
import os
import pymysql
import urllib.request
from num2words import num2words

#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="gapps" )
cursor = connection.cursor()

#login
server = GooglePlayAPI("en_US", "UTC")
server.login(None,None,4372181884517069262,'4Qez-s1eEJI4Myt1P_nw20zOpwj7209IFUWyVB76-Pyjb2ZIla5RGnatalrXTVDqi1IZ1A.')

#browse all categories
print("\nBrowse play store categories\n")
browse = server.browse()
# print(browse)
i=0#iterate over the "browse" dictionary
j=0
#fetch the ids of each category
for c in browse.get("category"):
    #print(c["name"])#name of category
    categ = browse["category"][i]["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
    print(categ)
    i=i+1
    
    #fetch the subcategories of each category
    categList = server.list(categ)
    for c in categList:
        print(c)
        #fetch the apps of each subcategories
        appList = server.list(categ, c)
        for app in appList:
            print(app["docid"])
            insert1 = "INSERT INTO main(aid, cat, subcat) VALUES(%s, %s, %s)"
            val=(app["docid"],categ,c)
            cursor.execute(insert1,val)
            j=j+1

            #getting details of each app
            # details = server.details(app["docid"])
            # print(details)
print("TOTAL APPS:", j)
connection.commit()
connection.close()