from os import link
import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
def getPharmacie(lien):
    req=Request(lien, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    nachrichten = soup.find_all("article", {"class": ["col-xs-12 column_in_grey","col-xs-12 column_in"]})
    pharmacies=[]
    for ul in nachrichten:
         if len(ul.findAll('h3'))==1 & len(ul.findAll('a',{'itemprop':'url'})[0]['href'])==1:
             pos=getPos("https://www.annuaire-gratuit.ma"+str(ul.findAll('a',{'itemprop':'url'})[0]['href']))
             if len(pos):
                 p=pos[0]
             pharmacies.append([str(ul.findAll('h3')[0].text),str(p)])
    return pharmacies

def getPos(lien):
    req=Request(lien, headers={'User-Agent': 'Mozilla/5.0'})
    web = urlopen(req).read()
    soup=BeautifulSoup(web,'lxml')
    nachrichten = soup.find_all("address")
    pharmacies=[]
    for ul in nachrichten:
         if len(ul.findAll('a'))==1:
             pharmacies.append(ul.findAll('a')[0]['href'])
    return pharmacies







url='https://www.annuaire-gratuit.ma/pharmacie-garde-maroc.html'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup=BeautifulSoup(webpage,'lxml')
nachrichten = soup.findAll('article')
links = []
for ul in nachrichten:
    print(len(ul.findAll('a')))
    if len(ul.findAll('a'))==1 & len(ul.findAll('p'))==1:
        pharmacies=getPharmacie("https://www.annuaire-gratuit.ma"+str(ul.findAll('a')[0]['href']))
        for i in pharmacies:
            links.append([ul.findAll('a')[0]['title'],ul.findAll('p')[0].text,i[0],i[1]])
print(links[0])

me=pd.DataFrame(links,columns=["ville","nombre","pharmacie","local"])
me.to_json('data.json')
print(me)