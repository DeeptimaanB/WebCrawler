import pandas as pd
import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
import ssl
from pygooglenews import GoogleNews

#ignoring ssl certificate errors
ctx= ssl.create_default_context()
ctx.check_hostname= False
ctx.verify_mode=ssl.CERT_NONE

data=dict()

data["Title"]=[]
data["Published"]=[]
data["Link"]=[]


i=0
occur=dict()
gn=GoogleNews()
sstring=input("Enter your search : ") #google query
wcounts=input("Enter the strings that you want to search : ") #Atleast one entry, it searches the count of ties the word exists in the page
words=[item for item in wcounts.split()]
for word in words:
    data[word]=[]


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
        data["Published"].append(item['published'])
        for word in words:
            results=soup.body.find_all(string=re.compile(word,re.IGNORECASE))
            data[word].append(len(results))
            l.append(len(results))
        title=soup.find("title")
        print(i)
        print(item['published'])
        print(title.get_text())
        data["Title"].append(title.get_text())
        data["Link"].append(j)
        occur[j]=l
        print(j)
        print( occur[j])
        print("\n")
    except:
        continue

df = pd.DataFrame(data)
print(df)
df.to_csv('data.csv', index=False)