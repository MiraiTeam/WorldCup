from players import *

class Team:
    def __init__(self,country,confederation,rank,players):
        self.country = country
        self.confederation = confederation
        self.rank = rank
        self.players = players   #players[position] = Player()
    def isHost(self):
        return 'host' in self.country

def GetTeamsInfo():
    #Players Info
    players = GetPlayers()
    pl = {}
    for p in players:
        if not pl.has_key(p.country):
            pl[p.country] = {}
        if not pl[p.country].has_key(p.position):
            pl[p.country][p.position] = []
        pl[p.country][p.position].append(p)

    file = open('teamsInfo.txt','r')
    teams = []
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
        teams.append(team)
    file.close()
    return teams

def GetTeamsClass(teams):
    teamsClass = {}
    for t in teams:
        if not teamsClass.has_key(t.confederation):
            teamsClass[t.confederation] = []
        teamsClass[t.confederation].append(t)

    for conf in teamsClass.keys():
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


teams = GetTeamsInfo()
#file = open('flags.txt','w')
#for t in sorted(teams,key = lambda Team:Team.country):
#    print t.country
#    file.write(t.country + '|\n')
#file.close()
#PrintTeamsInfo(teams)
#Seeding(teams)
