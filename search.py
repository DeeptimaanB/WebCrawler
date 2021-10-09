import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
import ssl
from pygooglenews import GoogleNews
import sqlite3
import datetime
import sys
import time

if(len(sys.argv)!=4):
    print("Arguments too less")
    exit()



#ignoring ssl certificate errors
ctx= ssl.create_default_context()
ctx.check_hostname= False
ctx.verify_mode=ssl.CERT_NONE

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

gn=GoogleNews()
sstring=sys.argv[1] #input("Enter your search : ") #google query
filename=sys.argv[2] #input("Enter you output filename: ")
sqlquery="DROP TABLE IF EXISTS \""+filename+"\";\n"
sqlquery=sqlquery+"CREATE TABLE "+filename+"("
sqlquery=sqlquery+'''
title VARCHAR(50),
published VARCHAR(30),
searched VARCHAR(30),
link VARCHAR(100),
'''
filen=filename
filename=filename+".csv"
wcounts=sys.argv[3] #input("Enter the strings that you want to search : ") #Atleast one entry, it searches the count of ties the word exists in the page
words=[item for item in wcounts.split()]
lenword=len(words)
i=1
for word in words:
    if(i==lenword):
        tsqlquery=word+''' INT(10)
'''
    else:
        tsqlquery=word+''' INT(10),
'''    
    i+=1
    sqlquery=sqlquery+tsqlquery
sqlquery=sqlquery+''');'''
i=0
cur.executescript(sqlquery)
sqlquery=""
search=gn.search(sstring, when="1y")
for item in search['entries']:
    j=item['links'][0]['href']
    try:
        l=[]
        html=urllib.request.urlopen(j, timeout=50, context=ctx).read()
        soup=BeautifulSoup(html,'html.parser')
        results=soup.body.find_all(string=re.compile(words[0],re.IGNORECASE))
        if(len(results)==0):
            continue
        i+=1
        for word in words:
            results=soup.body.find_all(string=re.compile(word,re.IGNORECASE))
            l.append(len(results))
        title=soup.find("title")
        print(i)
        print(item['published'])
        print(title.get_text())
        print(j)
        print(l)
        print("\n")
        title=title.get_text()
        ct = str(datetime.datetime.now())
        sqlquery="INSERT INTO "+filen+" VALUES (\""+title+"\" ,\""+item['published']+"\" ,\""+ct+"\" ,\""+j+"\" , "
        converted_list = [str(element) for element in l]
        joined_string = " , ".join(converted_list)
        sqlquery=sqlquery+joined_string+");"
        cur.executescript(sqlquery)  

    except:
        continue

print("Done")
time.sleep(5)