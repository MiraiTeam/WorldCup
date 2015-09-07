#coding=utf-8
import random
from arrange import *

def GetPlayers(team):
    players = []
    #FW,MF,DF,GK
    p = ['FW','MF','DF','GK']
    t = [(1,5,4,1),(2,4,4,1),(3,3,4,1)]
    random.shuffle(t)
    for z in t:
        try:
            for i in range(4):
                players += random.sample(team.players[p[i]],z[i])
            break
        except ValueError:
            players = []
    return players


def GetPlayersInfo(players):
    output = ''
    for p in players:
        output += '#%d, %s, %s\n' % (p.id,p.name,p.position)
    return output

def GetTeam(teams,country):
    for t in teams:
        if t.country == country:
            return t

def Emulate(teams,arrange):
    A = arrange.A
    B = arrange.B
    tA = GetTeam(teams,A)
    tB = GetTeam(teams,B)
    pA = GetPlayers(tA)
    pB = GetPlayers(tB)
    #print (tA.players['FW'][0])
    #print (tB.players['FW'][0])
    output = ''
    output += 'Group state:\n'
    output += A + ' vs ' + B + '\n'
    output += A + '\n'
    output += GetPlayersInfo(pA)
    output += B + '\n'
    output += GetPlayersInfo(pB)
    print output
    file = open('www.txt','w')
    file.writelines(output)
    file.close()

teams = GetTeamsInfo()
groups = Seeding(teams)
arrange = GetArrangement(groups,0)
print '--',len(teams)
for t in teams:
    if len(t.players) != 4:
        print 'aaa'
Emulate(teams,arrange[0][0])
