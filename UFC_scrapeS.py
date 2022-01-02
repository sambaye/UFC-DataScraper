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
import pandas as pd 
from scrapeSherdogP import *
from datetime import datetime
import ast 

def Sort(sub_li): 
  return (sorted(sub_li, key = lambda x: datetime.strptime(x[2],'%b-%d-%Y'),reverse=True)) 

def reverse(s):
  str = ""
  for i in s:
    str = i + str
  return str

def FixPercent(val):
 val2 =''
 valT =(val[2:])
 for i in range(len(valT)):
  if valT[i].isnumeric() == True:
   val2 += valT[i]
  elif valT[i] == '(':
   break
 return val2

def fixNull(data):
 ndata = []
 for i in range(len(Data)):
  if data[i] == '':
   ndata.append(0)
  else:
   ndata.append(data[i])
 return ndata

def makeLists(raw_data):
    wllist = []
    store = ""
    for i in range(len(str(raw_data))):
        if str(raw_data)[i] != '\n' and str(raw_data)[i] !='':
            store += str(raw_data)[i]
        else:
            wllist.append(store)
            store = ""
            continue
    return wllist

def DelLineSpace(raw_data):
    store = ""
    for i in range(len(raw_data)):
        if raw_data[i] != '\n' and raw_data[i] !='':
            store += raw_data[i]
        else:
            continue
    return store



def FixTwoD(raw_data):
    wllist = raw_data.copy()
    for i in range(len((raw_data))):
     date = reverse(reverse(raw_data[i][2])[:15])
     dateFormatted = datetime.strptime(date, '%b / %d / %Y')
     newDate = (dateFormatted.strftime('%b-%d-%Y'))
     wllist[i][2] =  newDate
    return wllist


def FixTags(raw_data):
    wllist = []
    store = ''
    for i in range(len(str(raw_data))):
        if str(raw_data)[i] != '\n':
            store += str(raw_data)[i]
        else:
            wllist.append(store)
            store = ""
            continue
    return reverse((reverse(str(wllist[1]))[:]))


def OnePedegree(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 WinLossInfo1 = []
 for i in   soup.find_all("tr",{"class":"even"}):
  WinLossInfo1.append((i.text))
 WinLossInfo2 = []
 for i in   soup.find_all("tr",{"class":"odd"}):
  WinLossInfo2.append((i.text))
 finalWinLoss = WinLossInfo1 + WinLossInfo2
 DynamicInfo = []
 for i in range(len(finalWinLoss)):
   DynamicInfo.append(makeLists(finalWinLoss[i])[1:])
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
 #print(TagsFinal)
 Dynamic = Sort(FixTwoD(DynamicInfo))
 return Dynamic


def LossType(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Info = []
 for i in   soup.find_all("span",{"class":"graph_tag"}):
  Info.append((i.text))
 LossData = Info[3:]
 KO = FixPercent(reverse(LossData[0]))
 DEC = FixPercent(reverse(LossData[2]))
 SUB = FixPercent(reverse(LossData[1]))
 return reverse(KO),reverse(DEC),reverse(SUB)


def WinType2(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Info = []
 for i in   soup.find_all("span",{"class":"graph_tag"}):
  Info.append((i.text))
 LossData = Info[0:3]
 KO = FixPercent(reverse(LossData[0]))
 DEC = FixPercent(reverse(LossData[2]))
 SUB = FixPercent(reverse(LossData[1]))
 return reverse(KO),reverse(DEC),reverse(SUB)








def Accuracy(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Accuracy = []
 for i in   soup.find_all("dd",{"class":"c-overlap__stats-value"}):
  Accuracy.append((i.text))
 for i in range(len(Accuracy)):
  if Accuracy[i] == '':
   Accuracy[i] = 0
  else:
   continue
 ACCURACY = ones((4))
 ACCURACY[:] = nan
 for i in range(len(Accuracy)):
  ACCURACY[i] = int(Accuracy[i])
 StrikesLanded = float(ACCURACY[0])
 TotalStrikes = float(ACCURACY[1])
 StrikingAccuracy = round(float(StrikesLanded/TotalStrikes),2)
 TakeDownLanded = float(ACCURACY[2])
 TakeDownAttempts = float(ACCURACY[3])
 TakeDownAccuracy = round(float(TakeDownLanded/TakeDownAttempts),2)
 return round(100*StrikingAccuracy,2),round(100*TakeDownAccuracy,2),TotalStrikes,TakeDownAttempts,StrikesLanded,TakeDownLanded
 #return round(100*StrikingAccuracy,2)

def SigStrikesPerMinute(Fighter): 
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther1 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-1"}):
  RateOther1.append((i.text))
 RateOther1 = array(RateOther1)
 if len(RateOther1) !=0 and RateOther1[0][1:5].replace('.','',1).isdigit()==True:
  Val = (RateOther1[0])
  return float(Val[1:5])
 else:
  Val = nan
  return Val

def SigStrikesAbsorbedPerMinute(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther2 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-2"}):
  RateOther2.append((i.text))
 RateOther2 = array(RateOther2)
 if len(RateOther2) !=0 and RateOther2[0][1:5].replace('.','',1).isdigit()==True:
 #if len(RateOther2) != 0 and RateOther2[0][1:5].isnumeric():
  Val = (RateOther2[0])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #if len(RateOther2) != 0:
 # Val = (RateOther2[0])
 #else:
 # Val = '11111111'
 #return float(Val[1:5])

def TakeDownPer15Minute(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther1 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-1"}):
  RateOther1.append((i.text))
 RateOther1 = array(RateOther1)
 if len(RateOther1) !=0 and RateOther1[1][1:5].replace('.','',1).isdigit()==True:
 #if len(RateOther1) != 0 and RateOther1[1][1:5].isnumeric()==True:
  Val = (RateOther1[1])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #print(RateOther1)
 #Val= (RateOther1[1])
 #return float(Val[1:5])

def SubmissionPer15Minute(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther2 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-2"}):
  RateOther2.append((i.text))
 RateOther2 = array(RateOther2)
 if len(RateOther2) !=0 and RateOther2[1][1:5].replace('.','',1).isdigit()==True:
 #if len(RateOther2) != 0 and RateOther2[1][1:5].isnumeric():
  Val = (RateOther2[1])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #Val = (RateOther2[1])
 #return float(Val[1:5])

def SigStrikeDefense(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther1 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-1"}):
  RateOther1.append((i.text))
 RateOther1 = array(RateOther1)
 if len(RateOther1) !=0 and RateOther1[2][1:5][0].isdigit()==True:
 #if len(RateOther1) !=0 and RateOther1[2][1:5].replace('.','',1).isdigit()==True:
 #if len(RateOther1) != 0:
 #and RateOther1[2][1:5].isnumeric():
  Val = (RateOther1[2])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #Val= (RateOther1[2])
 #return float(Val[1:5])


def TakeDownDefense(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther2 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-2"}):
  RateOther2.append((i.text))
 RateOther2 = array(RateOther2)
 #if len(RateOther2) !=0 and RateOther2[2][1:5].replace('.','',1).isdigit()==True:
 if len(RateOther2) !=0 and RateOther2[2][1:5][0].isdigit()==True:
 #if len(RateOther2) != 0: 
 #and RateOther2[2][1:5].isnumeric():
  Val = (RateOther2[2])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #Val = (RateOther2[2])
 #return float(Val[1:5])

def KDRatio(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther1 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-1"}):
  RateOther1.append((i.text))
 RateOther1 = array(RateOther1)
 if len(RateOther1) !=0 and RateOther1[3][1:5].replace('.','',1).isdigit()==True:
 #if len(RateOther1) != 0 and RateOther1[3][1:5].isnumeric()==True:
  Val = (RateOther1[3])
  return float(Val[1:5])
 else:
  Val = nan
  return Val
 #Val= (RateOther1[3])
 #return float(Val[1:5])

def AverageFightTime(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 RateOther2 = []
 for i in   soup.find_all("div",{"class":"c-stat-compare__group-2"}):
  RateOther2.append((i.text))
 RateOther2 = array(RateOther2)
 if len(RateOther2) != 0 and RateOther2[3][1:3].isnumeric():
  Val = (RateOther2[3])
  return float(Val[1:3])
 else:
  Val = nan
  return Val
 #Val = (RateOther2[3])
 #return float(Val[1:3])

def SigStrikeByPosition(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 SigByPositionWinType = []
 for i in   soup.find_all("div",{"class":"c-stat-3bar__value"}):
  SigByPositionWinType.append((i.text))
 SigByPositionWinType = array(SigByPositionWinType)
 if len(SigByPositionWinType) != 0:
  Standing = FixPercent(reverse(SigByPositionWinType[0]))
  Clinch = FixPercent(reverse(SigByPositionWinType[1]))
  Ground = FixPercent(reverse(SigByPositionWinType[2]))
  return reverse(Standing),reverse(Clinch),reverse(Ground)
 else:
  return nan,nan,nan 
def SigStrikeByTarget(Fighter):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Accuracy = []
 for i in   soup.find_all("dd",{"class":"c-overlap__stats-value"}):
  Accuracy.append((i.text))
 Accuracy = array(Accuracy)
 if len(Accuracy) != 0:
  TotalStrikes = float(Accuracy[0])
  SigByTarget = []
  TargetTags = ['head','body','leg']
  for i in range(3):
   for j in soup.find_all("text",{"id":"e-stat-body_x5F__x5F_"+TargetTags[i]+"_value"}):
    SigByTarget.append((j.text))
  SigByTarget = array(SigByTarget)
  Head = 100*float(SigByTarget[0])/TotalStrikes 
  Body = 100*float(SigByTarget[1])/TotalStrikes
  Leg  = 100*float(SigByTarget[2])/TotalStrikes
  return round(Head,0),round(Body,0),round(Leg,0)
 else:
  return nan,nan,nan
def WinType(Fighter,sher):
 time.sleep(2)
 source = requests.get("https://www.ufc.com/athlete/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 SigByPositionWinType = []
 for i in   soup.find_all("div",{"class":"c-stat-3bar__value"}):
  SigByPositionWinType.append((i.text))
 SigByPositionWinType = array(SigByPositionWinType)
 if len(SigByPositionWinType) != 0:
  KO = FixPercent(reverse(SigByPositionWinType[3]))
  DEC = FixPercent(reverse(SigByPositionWinType[4]))
  SUB = FixPercent(reverse(SigByPositionWinType[5]))
  return reverse(KO),reverse(DEC),reverse(SUB) ## Fix these
 else:
  KO,DEC,SUB = WinType2(sher) 
  return (KO),(DEC),(SUB) ## Fix these

def cleanRounds(raw_data):
 newRounds = []
 for i in range(len(raw_data)):
  if raw_data[i] <=  5:
   newRounds.append(raw_data[i])
  else:
   continue
 return asarray(newRounds)


def AveWLRound(raw_data):
 RoundsWin = []
 RoundsLoss = []
 for i in range(len(raw_data)):
  if raw_data[i][0] == 'win':
   RoundsWin.append(int(raw_data[i][4]))
  elif raw_data[i][0] == 'loss':
   RoundsLoss.append(int(raw_data[i][4]))
  else:
   continue
 RoundsWin = cleanRounds(asarray(RoundsWin))
 RoundsLoss = cleanRounds(asarray(RoundsLoss))
 return round(mean(RoundsWin),2),round(mean(RoundsLoss),2)

def WinLoss(raw_data):
 RoundsWin = []
 RoundsLoss = []
 for i in range(len(raw_data)):
  if raw_data[i][0] == 'win':
   RoundsWin.append(int(raw_data[i][4]))
  elif raw_data[i][0] == 'loss':
   RoundsLoss.append(int(raw_data[i][4]))
  else:
   continue
 win = len(RoundsWin)
 loss = len(RoundsLoss) 
 return win,loss




def Camp(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Camp = []
 for i in   soup.find_all("a",{"class":"association"}):
   Camp.append((i.text))
 return Camp

def WeightClass(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Class = []
 for i in   soup.find_all("h6",{"class":"item wclass"}):
   Class.append((i.text))
 return Class

def WeightS(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Weight = []
 for i in   soup.find_all("span",{"class":"item weight"}):
   Weight.append((i.text))
 return Weight

def HeightS(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Height = []
 for i in   soup.find_all("span",{"class":"item height"}):
   Height.append((i.text))
 return Height

def AgeS(Fighter):
 time.sleep(2)
 source = requests.get("https://www.sherdog.com/fighter/"+Fighter).text
 soup = BeautifulSoup(source, 'lxml')
 Age = []
 for i in   soup.find_all("span",{"class":"item birthday"}):
   Age.append((i.text))
 return Age




def GetStats(ufcTag,sherTag):
 ## Physical Atr
 Dynamics = OnePedegree(sherTag)
 win,loss = WinLoss(Dynamics)
 WL = str(win)+'-'+str(loss)
 Fighter = ufcTag
 Height = HeightS(sherTag)
 Height = Height[0][48:52]
 Weight = WeightS(sherTag)
 Weight = Weight[0][48:52]
 Age = AgeS(sherTag)
 Age = Age[0][63:65]
 # Pedegree
 Ped = load('PedigreeData/'+sherTag+'PED.npy')
 Depth = load('PedigreeData/'+sherTag+'twoLen.npy')
 CAMP = Camp(sherTag)
 newCamp = []
 if len(CAMP) != 0:
  newCamp.append(CAMP[0])
 else:
  newCamp.append("None")
 CLASS= WeightClass(sherTag)
 newClass = []
 if len(CLASS) != 0:
  newClass.append(CLASS[0])
 else:
  newClass.append("None")
 Wgt_Class = (FixTags(newClass[0]))
 Wgt_Class =(Wgt_Class[47:])
 ## Pedegree
 OnePedegree(sherTag)
 OneD = Ped[0] 
 TwoD = Ped[1]
 Pedigree = {'PEDIGREE':['Fighter','CAMP','W-L','OneD','TwoD','Depth'], 'Value':[str(Fighter),newCamp[0],WL,OneD,TwoD,Depth]}
 PEDIGREE = pd.DataFrame(Pedigree)
 PhysicalAtr = {'PHYSICAL ATTRIBUTES':['Fighter','Height','Weight','Wgt_Class','Age'], 'Value':[str(Fighter),Height,Weight,Wgt_Class,Age]}
 PHYSICALATR = pd.DataFrame(PhysicalAtr)
 ## Offense 
 StrikingAccuracy,TakeDownAccuracy,TotalStrikes,TakeDownAttempts,SigStrikeLanded,TakeDownLanded = Accuracy(Fighter)
 SigStrikePerMin = SigStrikesPerMinute(Fighter)
 TakeDownPer15min = TakeDownPer15Minute(Fighter)
 KnockDownRatio = KDRatio(Fighter)
 SubmissionPer15Min = SubmissionPer15Minute(Fighter)
 SigStrikeHead,SigStrikeBody,SigStrikeLeg = SigStrikeByTarget(Fighter)
 SigStrStanding,SigStrClinch,SigStrGround = SigStrikeByPosition(Fighter)
 WinKO,WinDEC,WinSUB =  WinType(Fighter,sherTag)
 Offense = {'OFFENSIVE STATS':['Fighter','StrikingAccuracy(%)','TotalStrikes', 'TakeDownAccuracy(%)','TakeDownAttempts', 'SigStrikePerMin','TakeDownPer15min','KnockDownRatio','SubmissionPer15Min','SigStrikeHead(%)','SigStrikeBody(%)','SigStrikeLeg(%)','SigStrStanding(%)','SigStrClinch(%)','SigStrGround(%)','SigStrikeLanded','TakeDownLanded','WinKO(%)', 'WinDEC(%)', 'WinSUB(%)'], 'Value':[str(Fighter),StrikingAccuracy, TotalStrikes,TakeDownAccuracy,TakeDownAttempts, SigStrikePerMin,TakeDownPer15min,KnockDownRatio,SubmissionPer15Min,SigStrikeHead,SigStrikeBody,SigStrikeLeg,SigStrStanding,SigStrClinch,SigStrGround,SigStrikeLanded,TakeDownLanded,WinKO,WinDEC,WinSUB]}
 OFFENSE = pd.DataFrame(Offense)
 ## Defense 
 LossKO,LossDEC,LossSUB = LossType(sherTag)
 SigStrikeDef = SigStrikeDefense(Fighter)
 SigStrAbsPerMin = SigStrikesAbsorbedPerMinute(Fighter)
 TakeDownDef = TakeDownDefense(Fighter)
 Defense = {'DEFENSIVE STATS':['Fighter','SigStrikeDef(%)','SigStrAbsPerMin','TakeDownDef(%)','LossKO(%)', 'LossDEC(%)', 'LossSUB(%)'], 'Value':[str(Fighter),SigStrikeDef,SigStrAbsPerMin,TakeDownDef,LossKO,LossDEC,LossSUB]}
 DEFENSE = pd.DataFrame(Defense)
 ## Esoteric
 CurrentDate =  datetime.today().strftime('%b-%d-%Y')
 AveWinRound, AveLossRound = AveWLRound(Dynamics)
 Last4 =  Dynamics[3][0]+'_'+Dynamics[2][0] +'_'+Dynamics[1][0] +'_'+Dynamics[0][0]  
 LastFought = Dynamics[0][2]
 AveFightTime = AverageFightTime(Fighter)
 Esoteric = {'ESOTERIC':['Fighter','AveFightTime(min)','Last4','AveWinRound','AveLossRound','LastFought','CurrentDate'], 'Value':[str(Fighter),AveFightTime,Last4,AveWinRound,AveLossRound,LastFought,str(CurrentDate)]}
 ESOTERIC = pd.DataFrame(Esoteric)
 ## average win time 
 ## average lose time 
 return PHYSICALATR,PEDIGREE,OFFENSE,DEFENSE,ESOTERIC

def NestList(lists):
 newList = []
 for i in range(0,len(lists),2):
  newList.append(lists[i:(i+2)]) 
 return newList

def Output(ufc_tag,sher_tag):
 ufc_tag1 =(str(ufc_tag[0]))
 ufc_tag1 = (reverse(reverse(ufc_tag1)[1:]))
 ufc_tag2 =(str(ufc_tag[1]))
 ufc_tag2 = (reverse(reverse(ufc_tag2)[1:]))
 sher_tag1 =(str(sher_tag[0]))
 sher_tag1 = (reverse(reverse(sher_tag1)[1:]))
 sher_tag2 =(str(sher_tag[1]))
 sher_tag2 = (reverse(reverse(sher_tag2)[1:]))
 ufc_tag1 = DelLineSpace(ufc_tag1)
 ufc_tag2 = DelLineSpace(ufc_tag2)
 sher_tag1 = DelLineSpace(sher_tag1)
 sher_tag2 = DelLineSpace(sher_tag2) 
 physicalatr,pedigree,offense,defense,esoteric =GetStats(ufc_tag1,sher_tag1) ## Good test case
 physicalatr2,pedigree2,offense2,defense2,esoteric2 =GetStats(ufc_tag2,sher_tag2) ## Good test case
 physicalatr2 = physicalatr2[['Value']]
 pedigree2 = pedigree2[['Value']]
 offense2 = offense2[['Value']]
 defense2 = defense2[['Value']]
 esoteric2 = esoteric2[['Value']]
 physicalatrComp = pd.concat([physicalatr, physicalatr2], axis=1)
 pedigreeComp = pd.concat([pedigree, pedigree2], axis=1)
 offenseComp  = pd.concat([offense, offense2], axis=1)
 defenseComp  = pd.concat([defense, defense2], axis=1)
 esotericComp = pd.concat([esoteric, esoteric2], axis=1)
 a = (physicalatrComp.to_string(index=False, header=True))
 b = (pedigreeComp.to_string(index=False, header=True))
 c = (offenseComp.to_string(index=False, header=True))
 d = (defenseComp.to_string(index=False, header=True))
 e = (esotericComp.to_string(index=False, header=True))
 NFighters = open("_"+ufc_tag1+"_"+ufc_tag2+"_"+"Data.txt","w")
 NFightersT = open("_all_Data.txt","a")
 NFightersT.write(a + "\n"+"\n" + b + "\n" + "\n"  + c +"\n" +"\n"+ d + "\n" +"\n"  +e +"\n" +"\n"   )
 NFighters.write(a+"\n"+b+"\n"+c+"\n"+d+"\n"+e)
 name1 ="_"+ufc_tag1+"_"+ufc_tag2+"_"+"physicalatrComp.pkl"
 name2 ="_"+ufc_tag1+"_"+ufc_tag2+"_"+"pedigreeComp.pkl"
 name3 ="_"+ufc_tag1+"_"+ufc_tag2+"_"+"offenseComp.pkl"
 name4 ="_"+ufc_tag1+"_"+ufc_tag2+"_"+"defenseComp.pkl"
 name5 ="_"+ufc_tag1+"_"+ufc_tag2+"_"+"esotericComp.pkl"
 
 physicalatrComp.to_pickle(name1) 
 pedigreeComp.to_pickle(name2)
 offenseComp.to_pickle(name3)
 defenseComp.to_pickle(name4)
 esotericComp.to_pickle(name5)
 # Print data to terminal:not needed but simply remove comments to do so
 '''
 print(physicalatrComp.to_string(index=False, header=True))
 print("")
 print(pedigreeComp.to_string(index=False, header=True))
 print("")
 print(offenseComp.to_string(index=False, header=True))
 print("")
 print(defenseComp.to_string(index=False, header=True))
 print("")
 print(esotericComp.to_string(index=False, header=True))
 '''
 return 0
def main():
 ufc_tag = open("Input/NFightersUFC.txt","r").readlines()
 UFC_TAG = NestList(ufc_tag)
 sher_tag = open("Input/NFightersSHER.txt","r").readlines()
 SHER_TAG = NestList(sher_tag)
 for i in range(len(UFC_TAG)):
  #print(UFC_TAG[i])
  #print(SHER_TAG[i])
  Output(UFC_TAG[i],SHER_TAG[i])

if __name__ == '__main__':
    main()

