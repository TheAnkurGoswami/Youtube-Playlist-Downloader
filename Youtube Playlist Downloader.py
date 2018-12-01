import bs4
import requests
import pytube as pt
import re
import os
import shelve

def Download(link,location):
    global file
    a=pt.YouTube(link)
    tagptrn=re.compile(r'itag="(\d+)"')
    itag=int(tagptrn.findall(str(a.streams.first()))[0])  #Best Quality
    print('DOWNLOADING: ',a.title)
    a.streams.get_by_itag(itag).download(location)
    file['count']+=1

if os.path.isfile('data.bak'):
    file=shelve.open('data',writeback=True)
    
else:    
    #--------------------------------CREATING FILE & PARSING THE PAGE--------------------------
    file=shelve.open('data',writeback=True)
    address=input('Enter Playlist address: ')
    location=input('Enter Location to save or Press \'Enter\' to skip: ')
    ReqObject=requests.get(address)
    Object=bs4.BeautifulSoup(ReqObject.content,'html.parser')
    
    
    #----------------------------------SETTING PLAYLIST LOCATION-------------------------------
    if location=='':
        location=os.getcwd()
    playlist_name=Object.findAll('title')[0].text  #Playlist name.
    location=location+'\\'+playlist_name          #Changing working directory.
    os.mkdir(location)                        #Creating Playlist name folder.

    
    #-------------------------------PLAYLIST VIDEOS EXTRACTION---------------------------------
    pattern=re.compile(r'(/watch\?v=\S+)')
    URLs=[]
    for i in pattern.findall(str(Object)):
        URLs.append(i[:i.find('&amp;')])
    URLs=list(set(URLs))
    Total=len(URLs)
    
    #--------------------------------------SAVING CURRENT STATE---------------------------------
    file['URLs']=URLs
    file['status']=[0]*Total
    file['count']=0
    file['location']=location
    file['Total']=Total
    
    #-------------------------CHECKING IF VIDEO IS DOWNLOADED OR NOT--------------------------
os.system('cls')
i=0   
while i<file['Total']:
    os.system('cls')
    print('Progress: %.2f'%((file['count']*100)/file['Total']),'%\n')
    if file['status'][i]:    #If video is already downloaded.
        pass
    else:
        Download(r'http://www.youtube.com'+file['URLs'][i],file['location'])
        file['status'][i]=1
    os.system('cls')
    print('Progress: %.2f'%((file['count']*100)/file['Total']),'%\n')
    i+=1
if all(file['status']):
    file.close()
    os.remove('data.bak')
    os.remove('data.dat')
    os.remove('data.dir')
    print('\n\nPlaylist Download Complete.')
else:
    file.close()
