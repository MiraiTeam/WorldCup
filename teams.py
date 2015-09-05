class Team:
    def __init__(self,country,confederation,rank):
        self.country = country
        self.confederation = confederation
        self.rank = rank

def GetTeamsInfo():
    file = open('teamsInfo.txt','r')
    teams = []
    for line in file:
        sp = line.split(' ') # notice: the last element is '\n'
        country = ' '.join(sp[1:len(sp) - 3])
        confederation = sp[-3]
        rank = int(sp[-2])
        team = Team(country,confederation,rank)
        teams.append(team)
    file.close()
    return teams

def PrintTeamsInfo(teams):
    #ckassify by confederation
    teamsClass = {}
    for t in teams:
        if not teamsClass.has_key(t.confederation):
            teamsClass[t.confederation] = []
        teamsClass[t.confederation].append(t)

    for conf in teamsClass.keys():
        teamsClass[conf] = sorted(teamsClass[conf],key = lambda Team : Team.country)

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
PrintTeamsInfo(teams)
