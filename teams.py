from players import *

class Team:
    def __init__(self,country,confederation,rank,players):
        self.country = country
        self.confederation = confederation
        self.rank = rank
        self.players = players   #players[position] = Player()
        #self.info = dict()   #gp,W,D,L,GF,GA,GD,Pts
        self.info = {'gp':'',
                    'w':0,
                    'd':0,
                    'l':0,
                    'gf':0,
                    'ga':0,
                    'gd':0,
                    'pts':0
                    }
    def isHost(self):
        return 'host' in self.country

def GetTeamsInfo():
    #Players Info
    players = GetPlayers()
    pl = {}
    for p in players:
        if p.country not in pl:
            pl[p.country] = {}
        if p.position not in pl[p.country]:
            pl[p.country][p.position] = []
        pl[p.country][p.position].append(p)

    file = open('teamsInfo.txt','r')
    teams = {}
    for line in file:
        line = line.strip('\n')
        sp = line.split(' ') # notice: the last element is '\n'
        if sp[-1] == '':
            del sp[-1]
        #line = id,name,conf,rank
        country = ' '.join(sp[1:len(sp) - 2])
        confederation = sp[-2]
        rank = int(sp[-1])
        team = Team(country,confederation,rank,pl[country])
        teams[country] = team
    file.close()
    return teams

def GetTeamsClass(teams):
    teamsClass = {}
    for t in teams.values():
        if t.confederation not in teamsClass:
            teamsClass[t.confederation] = []
        teamsClass[t.confederation].append(t)

    for conf in teamsClass:
        teamsClass[conf] = sorted(teamsClass[conf],key = lambda Team : Team.country)
    
    return teamsClass

def PrintTeamsInfo(teams):
    #ckassify by confederation

    teamsClass = GetTeamsClass(teams)

    output = '' # we make a output string buffer
    for conf in sorted(teamsClass.keys()):
        output += conf + ' (' + str(len(teamsClass[conf])) + ')\n'
        for t in teamsClass[conf]:
            output += '  ' + t.country + ' (' + str(t.rank) + ')\n'
    print output
    file = open('team32.txt','w')
    file.writelines(output)
    file.close()
