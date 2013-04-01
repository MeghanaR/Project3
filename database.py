import urllib2
import urlparse
import re
import os
import sys
from pymongo import MongoClient

crawling='http://en.wikipedia.org/wiki/List_of_Indian_independence_activists'
url2=urlparse.urlparse(crawling)
print url2.geturl()
req=urllib2.Request(crawling,headers={'User-Agent' : "Magic Browser"})
print req 
response=urllib2.urlopen(req)
msg=response.read()

linksregex=re.compile('<tr>\n<td><a href=".*" title=".*".*>.*</a></td>\n<td><a href=".*" title=".*">.*</a></td>')
links=linksregex.findall(msg)

links2regex=re.compile('<tr>\n<td><a href=".*" title=".*".*>.*</a></td>\n<td>.+</td>')
links2=links2regex.findall(msg)

genderregex=re.compile('<p>.*</p>')
maleregex=re.compile('(He|His)(.*?)')
femaleregex=re.compile('(She|Her)')

name=[]
region=[]
othername=[]
birthdate=[]
deathdate=[]
gender=[]
achievement=[]
structure=[]


def Region(links2):
        for link in links2:
                link=str(link)
                link=link.split('"')
                if len(link)>7:
                        st=link[7]
                        if st[0]=='/':
                                val=link[1]+';'+link[3]+';'+link[9]
                                structure.append(val)
                                region.append(link[9])
                                
                        else:
                                val=link[1]+';'+link[3]+';'+link[7]
                                structure.append(val)
                                region.append(link[7])
                                
                elif len(link)<6:
                        st=link[4].split('>')
                        st2=st[4].split('<')
                        val=link[1]+';'+link[3]+';'+st2[0]
                        structure.append(val)
                        region.append(st2[0])
                        
                else:
                        st=link[6].split('>')
                        st2=st[4].split('<')
                        val=link[1]+';'+link[3]+';'+st2[0]
                        structure.append(val)
                        region.append(st2[0])
                        
                name.append(link[3])

def DOB(msg):
        birthregex=re.findall('Date of birth</td>\n<td>.*</td>',msg)
        birth=str(birthregex).split('<td>')
        birth=birth[1].split('<')
        if birth[0]=='':
            
            birthdate.append('None')
        else:
            
            birthdate.append(birth[0])

def DOD(msg):
        '''Date of death'''
        deathregex=re.findall('Date of death</td>\n<td>.*</td>',msg)
        death=str(deathregex).split('<td>')
        death=death[1].split('<')
        if death[0]=='':
            
            deathdate.append('None')
        else:
            
            deathdate.append(death[0])

def Gender(msg):
        '''Gender'''
        genders=genderregex.findall(msg)
        male=maleregex.findall(str(genders))
        female=femaleregex.findall(str(genders))
        if len(male)<len(female):
            
            gender.append('female')
        else:
            
            gender.append('male')

def Achieve(msg):
        '''Achievements'''
        achievements=re.findall('Short description</td>\n<td>.*</td>',msg)
        achieve=str(achievements).split('<td>')
        achieve=achieve[1].split('<')
        if achieve[0]=='':
            
            achievement.append('None')
        else:
            
            achievement.append(achieve[0])

def Other(msg):
        othernamesregex=re.findall('Alternative names</td>\n<td>.*</td>',msg)
        if othernamesregex==[]:
                othername.append('None')
                birthdate.append('None')
                deathdate.append('None')
                gender.append('None')
                achievement.append('None')
                
                return 0
        else:
                othernames=str(othernamesregex).split('<td>')
                othernames=othernames[1].split('<')
                if othernames[0]=='':
                    
                    othername.append('None')
                else:
                    st=othernames[0]
                    if st[1]=='x':
                        
                        othername.append('None')
                    else:
                        
                        othername.append(othernames[0])
                return 1




Region(links2)

print "Crawling wikipedia..............."
for struc in structure:
    site=(struc.split(';'))[0]
    site='http://en.wikipedia.org'+site
    req=urllib2.Request(site,headers={'User-Agent' : "Magic Browser"}) 
    response=urllib2.urlopen(req)
    msg=response.read()
    val=Other(msg)
    if val==1:
            DOB(msg)
            DOD(msg)
            Gender(msg)
            Achieve(msg)
            

ff=[]
i=0
while name and i<len(name):
        ff.append({'name':name[i],'gender':gender[i],'birthdate':birthdate[i],'deathdate':deathdate[i],'achievement':achievement[i],'region':region[i],'othername':othername[i]})        
        i+=1     

client=MongoClient()
db=client.fdb
collection = db.collection

ffs = db.ffs
ff_id = ffs.insert(ff)
print "Completion of crawling and inserting data into mongodb"




