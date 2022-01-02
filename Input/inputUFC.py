from bs4 import BeautifulSoup
import requests 
from urllib import *
from numpy import *
from collections.abc import Iterable
import webbrowser
import sys
from fake_useragent import UserAgent

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}


def reverse(s): 
  str = "" 
  for i in s: 
    str = i + str
  return str

def getName(name):
  namef = ""
  for i in range(len(name)):
   if name[i] != ' ':
    namef += name[i]
   else:
    break
  return reverse(namef)
 
def getTags(fighter):
 url = "https://google.com/search?q="+fighter
 res = requests.get(url, headers=header)
 #res.raise_for_status()
 soup = BeautifulSoup(res.text, 'html.parser')
 opp = soup.find('div',class_='kCrYT')
 return opp.text

Fighters = open("Fighters.txt","r").readlines()
NFighters = open("NFightersUFC.txt","w")

for i in range(len(Fighters)):
 gtag ="ufc.com "+ Fighters[i]
 opp = getTags(gtag)
 NFighters.write(opp+"\n")

NFighters.close()


