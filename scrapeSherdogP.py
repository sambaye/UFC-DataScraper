from bs4 import BeautifulSoup
import requests 
from urllib import *
from numpy import *
from collections.abc import Iterable
import time
from fake_useragent import UserAgent
import multiprocessing
import concurrent.futures
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

def flatten(L):
        for item in L:
            if isinstance(item,list):
                for subitem in item:
                    yield subitem
            else:
                yield item


def makeLists(raw_data):
    wllist = []
    store = ""
    for i in range(len(str(raw_data.text))):
        if str(raw_data.text)[i] != '\n':
            store += str(raw_data.text)[i]
        else:
            wllist.append(store)
            store = ""
            continue
    return wllist


def makeLists2(raw_data):
    wllist = []
    store = ""
    for i in range(len(str(raw_data))):
        if str(raw_data)[i] != '\"':
            store += str(raw_data)[i]
        else:
            break
    return store

def OppLists(OppList):
 Opponents = []
 for i in range(1,len(OppList),8):
  Opponents.append(OppList[i])
 return Opponents


def winLoss(OppList):
 win = OppList.count(' W')
 loss = OppList.count(' L')
 draw = OppList.count(' D')
 NC = OppList.count(' N')
 return win,loss,draw,NC 

def linkLister(links):
 linkList = []
 for tag in links:
    link = tag.get('href',None)
    if link is not None:
        linkList.append(link) 
 return linkList

def makePLlist(llist):
 nlist = []
 for i in range(len(llist)):
  tag =(llist[i][1:8])
  if tag == 'fighter':
   nlist.append(llist[i][9:])
  else:
   continue
 return nlist

def formatName(name):
 holder = ''
 for i in range(len(name)):
  if name[i] != ' ':
   holder+= name[i] 
  else:
   holder+='-'
 return holder

def formatNameR(name):
 holder = 0
 for i in range(1,len(name)+1,1):
  if name[(0-(i))] != '-':
   holder += 1
  else:
    break
 return holder




def formatNameList(namelist):
 nnamelist = []
 for i in range(len(namelist)):
  nnamelist.append(formatName(namelist[i]))
 return nnamelist


def formatFlist(nnamelist,fllist):
 indexlist = []
 for i in range(len(fllist)):
  reallen =(len(fllist[i])-formatNameR(fllist[i])) - 1
  TF = (fllist[i][:reallen] in nnamelist)
  if TF == True:
   indexlist.append(i)
  else:
   continue 
  #print (reallen)
  #break
 return array(indexlist)



def getTags(fighterTag):
 atags = []
 newF = fighterTag[18:]
 tag = ""
 for i in range(len(newF)):
  if newF[i] != '\"':
   tag += newF[i]
  else:
   break
 return tag




def OnePedegree(Fighter):
 time.sleep(5)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 time.sleep(5)
 #opponentsRaw = soup.findAll("table", {"class": "dataTable"})
 WinRaw = soup.find_all("span", {"class": "final_result win"})
 LossRaw = soup.find_all("span", {"class": "final_result loss"})
 Draw = soup.find_all("span", {"class": "final_result draw"})
 NC = soup.find_all("span", {"class": "final_result no_contest"})
 W  =  ((len(WinRaw)))
 L = (len(LossRaw))
 D = (len(Draw))
 NC   =   (len(NC))
 stats = array((W,L,D,NC))
 Info = []
 for i in   soup.find_all("td",{"class":None}):
  Info.append((i.findAll("a")))
 fighterTag = "fighter"
 Tag = []
 for i in range(len(Info)):
  if len(Info[i]) != 0:
   Tag.append(str(Info[i][0]))
 FighterTag = []
 for i in range(len(Tag)):
   if Tag[i][10:17] == fighterTag:
    FighterTag.append(Tag[i])
   else:
    continue
 TagsFinal = []
 for i in range(len(FighterTag)):
  TagsFinal.append(getTags(FighterTag[i])) 
 return stats,TagsFinal
 
  

def TwoPedegree(opplist):
 twoD = []
 opplist2D = []
 Fighter = []
 for i in range(len(opplist)):
  Fighter.append(opplist[i])
 time.sleep(5)
 with concurrent.futures.ProcessPoolExecutor() as executor:
  results = executor.map(OnePedegree,Fighter)
  for result in results:
   opplist2D.append(result[1])
   twoD.append(result[0])
 time.sleep(5)
 return array((twoD)),opplist2D

def ThreePedegree(opplist2D):
 opplistHold = []
 opplist3D = []
 for i in range(len(opplist2D)):
  for j in range(len(opplist2D[i])):
   Fighter = opplist2D[i][j]
   opplistHold.append(Fighter)
 threeD = []
 time.sleep(5)
 with concurrent.futures.ProcessPoolExecutor() as executor:
  results = executor.map(OnePedegree,opplistHold)
  for result in results:
   #opplist3D.append(result[1])
   threeD.append(result[0])
 time.sleep(5)
 return array((threeD))


def makePed(oneD,twoD,threeD):
    oneDtot = oneD[0] + oneD[1]
    twoD = sum(twoD,0)
    twoDtot = twoD[0] + twoD[1]
    threeD = sum(threeD,0)
    threeDtot = threeD[0] + threeD[1]
    oneDped = float(oneD[0]/oneDtot)
    twoDped = float(twoD[0]/twoDtot)
    threeDped = float(threeD[0]/threeDtot)
    return oneDped,twoDped,threeDped

def makePed2(oneD,twoD):
    oneDtot = oneD[0] + oneD[1]
    twoD = sum(twoD,0)
    twoDtot = twoD[0] + twoD[1]
    oneDped = float(oneD[0]/oneDtot)
    twoDped = float(twoD[0]/twoDtot)
    return oneDped,twoDped

def Total(tag):
 tag = str(tag)[:len(tag)-1]
 #print(tag)
 stats,opplist = OnePedegree(tag) ## Good test case
 #print(stats)
 twoD,opplist2D = TwoPedegree(opplist)
 #print(len(twoD))
 
 #time.sleep(2)
 #threeD = ThreePedegree(opplist2D)
 #print(len(threeD))
 time.sleep(2)
 one,two = makePed2(stats,twoD)
 save(tag+'PED.npy',array((one,two)))
 save(tag+'twoLen.npy',array((len(twoD))))
 #save(tag+'threeLen.npy',array((len(threeD))))
 return 0 

def main():
 Fighters = open("Input/NFightersSHER.txt","r").readlines()
 for i in range(len(Fighters)):
  Total(Fighters[i])
  time.sleep(5)


if __name__ == '__main__':
    main()

