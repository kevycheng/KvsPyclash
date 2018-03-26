# -- coding:UTF-8 --
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path

gColor = True

try:
    from smartAutoBuildUtil import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print "[WARNING]: need colorama module"
    gColor = False
    pass

class bcolors:
    if(gColor == True):
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    else:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''

def drawOptions(titles, options, bCancelIndex = False):

    opTitle = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U"]

    if(options == None):
        print "!!!wrong argument!!!"
        return

    optionslen = len(options)
    if(optionslen == 0):
        return

    c = "+"
    h = "-"
    v = "|"
    wLengh = 68

    print "\n"
    print c + "-" * wLengh + c
    if(bCancelIndex==False):
        print v + bcolors.WARNING + titles.center(wLengh) + bcolors.ENDC +v
    else:
        print v + bcolors.OKGREEN + titles.center(wLengh) + bcolors.ENDC +v

    print c + "-" * wLengh + c
    #draw margin
    for i in range(1, 2):
        print v + " " * wLengh + v

    #draw options
    idx = 0
    for op in options:
        if(bCancelIndex==False):
            mystring = " %s) %s" % (opTitle[idx],op)
        else:
            mystring = " %s" % (op)

        print v + mystring.ljust(wLengh) + v
        idx = idx +1
    #draw margin
    for i in range(1, 2):
        print v + " " * wLengh + v
    print c + "-" * wLengh + c

    pass

def getmemberbyid(memberid):
    
    member_content = []
    
    # remove special char
    person_id = memberid.replace("#", "")

    person_page = 'https://www.clashofstats.com/players/' + person_id + '/profile'
    
    res_person = requests.get(person_page)
    soup_person = BeautifulSoup(res_person.text, "lxml")

    title = soup_person.find_all('span', attrs={'class': 'middle'})
    if(len(title)):
        member_content.append(title[0].text)
    else:
        member_content.append("None")
    
    th_levels = soup_person.find_all('div', attrs={'class': 'th-level'})
    if(len(th_levels)):
        member_content.append(th_levels[0].text.replace("Town Hall", ""))
    else:
        member_content.append("None")
    
    queenlevel = 0
    hero_levels = soup_person.find_all(attrs={"data-tooltip": "Archer Queen (Max for TH: 50, Max: 50)"})
    if(len(hero_levels)==0):
        hero_levels = soup_person.find_all(attrs={"data-tooltip": "Archer Queen (Max for TH: 40, Max: 50)"})
    if(len(hero_levels)==0):
        hero_levels = soup_person.find_all(attrs={"data-tooltip": "Archer Queen (Max for TH: 30, Max: 50)"})

    if(len(hero_levels)>0):
        member_content.append(hero_levels[0].text)
    else:
        member_content.append("0")

    hero_levels = soup_person.find_all(attrs={"data-tooltip": "Barbarian King (Max for TH: 50, Max: 50)"})
    if(len(hero_levels)==0):
        hero_levels = soup_person.find_all(attrs={"data-tooltip": "Barbarian King (Max for TH: 40, Max: 50)"})
    if(len(hero_levels)==0):
        hero_levels = soup_person.find_all(attrs={"data-tooltip": "Barbarian King (Max for TH: 30, Max: 50)"})
    if(len(hero_levels)==0):
        hero_levels = soup_person.find_all(attrs={"data-tooltip": "Barbarian King (Max for TH: 10, Max: 50)"})

    if(len(hero_levels)>0):
        member_content.append(hero_levels[0].text)
    else:
        member_content.append('0')

    hero_levels = soup_person.find_all(attrs={"data-tooltip": "Grand Warden (Max for TH: 20, Max: 20)"})

    if(len(hero_levels)>0):
        member_content.append(hero_levels[0].text)
    else:
        member_content.append('0')
    
    return member_content

def pyclan():
    pass

def collectmemberbyclanid(clan_id, clan_name):
    
    clan_member = []
    
    clan_page = 'https://www.clashofstats.com/clans/' + clan_id + '/members'

    print(clan_name)
    print(clan_page)

    res = requests.get(clan_page)
    soup = BeautifulSoup(res.text,'lxml')
    table = soup.find_all('table')

    dfs = pd.read_html(res.text)
    df = dfs[0]
    #df

    members = df.iloc[0:50, 3]
    print("member count: " + str(len(members)))

    for i in range(0,len(members)):
        #print('=======')
        id1 = members[i].split('#')
        name = id1[0].split('access_time')[0]
    
        length = len(id1)
        possibleid = id1[length-1]
        realid = possibleid.split('Member')[0].split('Elder')[0].split('Co-Leader')[0].split('Leader')[0]
        #print(name)
        #print(realid)
        clan_member.append(realid)

    return clan_member

def pymember():

    clan_id_list = []
    clan_name_list = []
    clan_merge = []

    if not os.path.isfile("clanlist.txt"):
        print("[ERROR] clanlist.txt not exist")
        return

    f = open("clanlist.txt", "r")
    exec(f)

    # check both length
    if not len(clan_id_list) == len(clan_name_list):
        print("[ERROR] clan length not match, please check clanlist.txt. ")
        return

    titles = "1. Clan Selection"
    drawOptions(titles, clan_name_list)

    anw = raw_input ("Enter Your Choice [A/B/C/D...]? : ")

    clan_member = []

    # convert char to int
    sel = ord(anw.lower()) - ord('a')
    if(sel < len(clan_id_list)):
        clan_id = clan_id_list[sel]
        clan_name = clan_name_list[sel]
        clan_member = collectmemberbyclanid(clan_id, clan_name)
    else:
        print("out of range, collect all")
        members = []
        for i in range(0, len(clan_id_list)):
            clan_id = "00000000"
            clan_name = "All"
            members = collectmemberbyclanid(clan_id_list[i], clan_name_list[i])
            clan_member.extend(members)

    # hard code testing
    #clan_id = 'QUPRQGRP'

#    clan_page = 'https://www.clashofstats.com/clans/' + clan_id + '/members'

#    print(clan_name)
#    print(clan_page)

#    res = requests.get(clan_page)
#    soup = BeautifulSoup(res.text,'lxml')
#    table = soup.find_all('table')

#    dfs = pd.read_html(res.text)
#    df = dfs[0]
#    #df

#    members = df.iloc[0:50, 3]
#    print("member count: " + str(len(members)))

#    clan_member = []
      
#    for i in range(0,len(members)):
#        #print('=======')
#        id1 = members[i].split('#')
#        name = id1[0].split('access_time')[0]
#    
#        length = len(id1)
#        possibleid = id1[length-1]
#        realid = possibleid.split('Member')[0].split('Elder')[0].split('Co-Leader')[0].split('Leader')[0]
#        #print(name)
#        #print(realid)
#        clan_member.append(realid)
    
    print('[start]')
     
    idlist = []
    namelist = []
    thlist = []
    kinglist = []
    queenlist = []
    wardenlist = []

    for i in range(0, len(clan_member)):
        print("======================="+ str(i) + " from " + str(len(clan_member)-1) + "=== " +clan_member[i] + " ===")
        #print(clan_member[i])
        realid = clan_member[i]

        nParsingCount = 0;

        #use while loop to prevent request error
        while True:
            print("parsing...")
            membercontent = getmemberbyid(realid)
            nParsingCount = nParsingCount+1    
            if(membercontent[0]!='None'):
                #print(membercontent)
                memberdf = pd.DataFrame(np.array(membercontent).reshape(1,5), columns = ['Name', 'TH','Queen', 'King', 'Warden'])
                print memberdf
                break
            if(nParsingCount > 10):
                break
            
        idlist.append(realid)
        namelist.append(membercontent[0])
        thlist.append(membercontent[1])
        kinglist.append(membercontent[2])
        queenlist.append(membercontent[3])
        wardenlist.append(membercontent[4])
    
    print("=======================end")

    BabyDataSet = list(zip(idlist,namelist,thlist,kinglist,queenlist,wardenlist))
    BabyDataSet
    df = pd.DataFrame(data = BabyDataSet, columns=['id', 'name', 'th lv', 'king', 'queen', 'warden'])
    #df

    outputfile = 'memberdetail_' + clan_id +'_'+ clan_name + '.csv'
    df.to_csv(outputfile, encoding='utf_8_sig')

    print("=======================saved")

    pass

def main():
    pymember()
    pass

if __name__ == '__main__':

    main()
    raw_input("Press Enter to exit")
    pass